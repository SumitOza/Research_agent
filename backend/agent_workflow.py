import logging
import time
import json
import re
from typing import Dict, List, TypedDict
from pydantic import BaseModel, Field, ValidationError
from langchain_cerebras import ChatCerebras
from langgraph.graph import StateGraph, END

# Configuration Constants
DEFAULT_NUM_INTERVIEW = 4
DEFAULT_NUM_QUESTIONS = 4
MAX_RETRIES = 3
TIMEOUT_SECONDS = 30

# Enhanced logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- PYDANTIC MODELS (Fixed Typo: backgroud -> background) ---
class Persona(BaseModel):
    name: str = Field(..., description="Full name of the Persona")
    age: int = Field(..., description="Age in Years")
    job: str = Field(..., description="Job Title or role")
    traits: List[str] = Field(..., description="3-4 personality traits")
    communication_style: str = Field(..., description="How this person communicates")
    background: str = Field(..., description="One background detail shaping their perspective")

class PersonaList(BaseModel):
    personas: List[Persona] = Field(..., description="List of generated personas")

class InterviewState(TypedDict):
    research_question: str
    target_demographic: str
    num_interviews: int
    num_questions: int
    interview_questions: List[str]
    personas: List[Persona]
    current_persona_index: int
    current_question_index: int
    current_interview_history: List[Dict]
    all_interviews: List[Dict]
    synthesis: str

# --- HELPER FUNCTIONS ---

def clean_and_parse_json(raw_output: str):
    """Robustly clean and parse JSON from AI output"""
    # 1. Strip Markdown code blocks
    text = re.sub(r'```json\s*', '', raw_output, flags=re.IGNORECASE)
    text = re.sub(r'```\s*', '', text)
    
    # 2. Locate the JSON object
    start = text.find('{')
    end = text.rfind('}') + 1
    if start == -1 or end == 0:
        raise ValueError("No JSON object found in response")
    
    json_str = text[start:end]
    
    # 3. Parse JSON
    try:
        return json.loads(json_str)
    except json.JSONDecodeError:
        # Fallback: Try to fix common trailing comma issues
        json_str = re.sub(r',\s*}', '}', json_str)
        json_str = re.sub(r',\s*]', ']', json_str)
        return json.loads(json_str)

def parse_questions_from_response(raw_output: str) -> List[str]:
    """Parse questions from AI response"""
    questions = []
    # Strategy 1: Try JSON parsing
    try:
        clean_text = raw_output.strip().replace("```json", "").replace("```", "")
        start = clean_text.find('[')
        end = clean_text.rfind(']') + 1
        if start != -1:
            import ast
            questions = ast.literal_eval(clean_text[start:end])
            if questions: return questions
    except:
        pass
    
    # Strategy 2: Line-by-line parsing
    lines = raw_output.strip().split('\n')
    for line in lines:
        # Clean numbering (1., 2.) and bullets (-, *)
        clean = re.sub(r'^[\d\-\.\)\*\s]+', '', line).strip().strip('"\'')
        if len(clean) > 10 and '?' in clean:
            questions.append(clean)
            
    return questions[:10] # Limit to sensible amount

def ask_ai(llm, prompt: str) -> str:
    response = llm.invoke([
        {"role": "system", "content": "You are a helpful research assistant."}, 
        {"role": "user", "content": prompt}
    ])
    return response.content

# --- PROMPTS ---

question_gen_prompt = """Generate exactly {num_questions} interview questions about: {research_question}. 
Rules:
- Open-ended questions only
- Clear and conversational
- One question per line
- No numbering or bullet points
"""

# Fixed prompt to use 'background' correctly
persona_prompt = (
    "Generate exactly {num_personas} unique personas for an interview.\n"
    "Target Demographic: '{demographic}'.\n"
    "Respond with ONLY a valid JSON object using this schema:\n"
    "{{\n"
    "  \"personas\": [\n"
    "    {{\n"
    "      \"name\": \"Name\",\n"
    "      \"age\": 30,\n"
    "      \"job\": \"Job\",\n"
    "      \"traits\": [\"Trait1\", \"Trait2\"],\n"
    "      \"communication_style\": \"Casual\",\n"
    "      \"background\": \"Brief background info\"\n"
    "    }}\n"
    "  ]\n"
    "}}"
)

interview_prompt = """You are playing the role of {name}, a {age}-year-old {job}.
Traits: {traits}.
Background: {background}.

Question: {question}

Answer strictly in character. Be realistic, honest, and concise (2-3 sentences).
"""

synthesis_prompt = """Analyze these {num} interviews about "{topic}".
TRANSCRIPTS:
{transcripts}

Provide a concise analysis:
1. Key Themes
2. Diverse Perspectives
3. Pain Points
4. Recommendations
"""

# --- WORKFLOW NODES ---

def config_node(state: InterviewState, llm) -> Dict:
    print(f"\n🔧 Configuring: {state['research_question']}")
    response = ask_ai(llm, question_gen_prompt.format(
        num_questions=state['num_questions'], 
        research_question=state['research_question']
    ))
    questions = parse_questions_from_response(response)
    if not questions: raise ValueError("Failed to generate questions")
    print(f"[✓] Generated {len(questions)} questions")
    return {"interview_questions": questions}

def persona_generation_node(state: InterviewState, llm) -> Dict:
    print(f"\n[👥] Creating {state['num_interviews']} personas...")
    
    for attempt in range(3):
        try:
            response = llm.invoke([{'role': 'user', 'content': persona_prompt.format(
                num_personas=state['num_interviews'],
                demographic=state['target_demographic']
            )}])
            
            # Clean and Parse
            data = clean_and_parse_json(response.content)
            
            # Validate
            validated = PersonaList.model_validate(data)
            
            print(f"[✓] Created {len(validated.personas)} personas")
            return {
                "personas": validated.personas,
                "current_persona_index": 0,
                "current_question_index": 0,
                "all_interviews": []
            }
        except Exception as e:
            print(f"[X] Attempt {attempt+1} failed: {e}")
            
    raise RuntimeError("Failed to generate valid personas")

def interview_node(state: InterviewState, llm) -> Dict:
    persona = state['personas'][state['current_persona_index']]
    question = state['interview_questions'][state['current_question_index']]
    
    print(f"\n[💬] {persona.name} (Q{state['current_question_index']+1}): {question}")
    
    answer = ask_ai(llm, interview_prompt.format(
        name=persona.name, age=persona.age, job=persona.job,
        traits=", ".join(persona.traits), background=persona.background,
        question=question
    ))
    print(f"[A]: {answer}")
    
    history = state.get('current_interview_history', []) + [{"question": question, "answer": answer}]
    
    # Logic to advance to next question or next persona
    if state['current_question_index'] + 1 >= len(state['interview_questions']):
        # Finished this persona
        completed_interview = {
            "persona": persona.model_dump(),
            "responses": history
        }
        return {
            "all_interviews": state['all_interviews'] + [completed_interview],
            "current_interview_history": [],
            "current_question_index": 0,
            "current_persona_index": state['current_persona_index'] + 1
        }
    
    return {
        "current_interview_history": history,
        "current_question_index": state['current_question_index'] + 1
    }

def synthesis_node(state: InterviewState, llm) -> Dict:
    print("\n[⧖] Synthesizing results...")
    summary = ""
    for i in state['all_interviews']:
        p = i['persona']
        summary += f"\nPersona: {p['name']} ({p['job']})\n"
        for r in i['responses']:
            summary += f"Q: {r['question']}\nA: {r['answer']}\n"
            
    synthesis = ask_ai(llm, synthesis_prompt.format(
        num=len(state['all_interviews']),
        topic=state['research_question'],
        transcripts=summary
    ))
    
    print("="*40 + "\nINSIGHTS\n" + "="*40)
    print(synthesis)
    return {"synthesis": synthesis}

def interview_router(state: InterviewState) -> str:
    if state['current_persona_index'] >= len(state['personas']):
        return "synthesize"
    return "interview"

# --- MAIN EXECUTION ---

def execute_research_workflow(api_key: str, research_topic: str, target_demographic: str, sample_size: int, num_questions: int) -> Dict:
    try:
        llm = ChatCerebras(model="llama3.3-70b", max_tokens=800, api_key=api_key)
        
        workflow = StateGraph(InterviewState)
        workflow.add_node("config", lambda s: config_node(s, llm))
        workflow.add_node("personas", lambda s: persona_generation_node(s, llm))
        workflow.add_node("interview", lambda s: interview_node(s, llm))
        workflow.add_node("synthesize", lambda s: synthesis_node(s, llm))
        
        workflow.set_entry_point("config")
        workflow.add_edge("config", "personas")
        workflow.add_edge("personas", "interview")
        workflow.add_conditional_edges("interview", interview_router, {"interview": "interview", "synthesize": "synthesize"})
        workflow.add_edge("synthesize", END)
        
        app = workflow.compile()
        
        final = app.invoke({
            "research_question": research_topic,
            "target_demographic": target_demographic,
            "num_interviews": sample_size,
            "num_questions": num_questions,
            "all_interviews": []
        }, {"recursion_limit": 150})  # <--- ADD THIS PART
        
        return {
            "success": True,
            "synthesis": final["synthesis"],
            "interviews": final["all_interviews"],
            "questions": final["interview_questions"]
        }
        
    except Exception as e:
        logger.error(f"Workflow failed: {e}")
        return {"success": False, "error": str(e)}