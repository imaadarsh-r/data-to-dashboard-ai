"""LLM Service for dashboard generation using LangChain + Groq"""
import json
import re
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_core.output_parsers import StrOutputParser
from app.config import settings
from app.prompts import SYSTEM_PROMPT, build_user_prompt

class LLMService:
    """Service for interacting with Groq API using LangChain"""
    
    def __init__(self):
        """Initialize LangChain ChatGroq client"""
        # Initialize ChatGroq with LangChain
        self.llm = ChatGroq(
            api_key=settings.GROQ_API_KEY,
            model_name=settings.GROQ_MODEL,
            temperature=settings.TEMPERATURE,
            max_tokens=settings.MAX_TOKENS,
        )
        
        # Create prompt template
        self.prompt_template = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(SYSTEM_PROMPT),
            HumanMessagePromptTemplate.from_template("{user_prompt}")
        ])
        
        # Create output parser
        self.output_parser = StrOutputParser()
        
        # Create the LangChain chain
        self.chain = self.prompt_template | self.llm | self.output_parser
        
        self.model = settings.GROQ_MODEL
    
    def generate_dashboard(self, json_data_str: str, user_instructions: str, temperature: float = None) -> dict:
        """
        Generate dashboard HTML from JSON data and user instructions using LangChain
        
        Args:
            json_data_str: JSON data as string
            user_instructions: User's design instructions
            temperature: Optional temperature override (0.0-2.0)
            
        Returns:
            dict with 'html', 'tokens_used', and 'model' keys
        """
        import time
        import logging
        
        logger = logging.getLogger(__name__)
        start_time = time.time()
        
        try:
            # Step 1: Parse JSON
            logger.info("🔍 Step 1: Parsing JSON data...")
            parse_start = time.time()
            json_data = json.loads(json_data_str)
            parse_time = time.time() - parse_start
            logger.info(f"✅ JSON parsed successfully in {parse_time*1000:.2f}ms")
            logger.debug(f"   Data keys: {list(json_data.keys())}")
            
            # Step 2: Build prompt
            logger.info("📝 Step 2: Building user prompt...")
            prompt_start = time.time()
            user_prompt = build_user_prompt(json_data, user_instructions)
            prompt_time = time.time() - prompt_start
            prompt_length = len(user_prompt)
            logger.info(f"✅ Prompt built in {prompt_time*1000:.2f}ms ({prompt_length} chars)")
            logger.debug(f"   Prompt preview: {user_prompt[:200]}...")
            
            # Step 3: Configure temperature
            temp = temperature if temperature is not None else settings.TEMPERATURE
            logger.info(f"🌡️  Step 3: Temperature set to {temp}")
            
            # Step 4: Create/select chain
            logger.info("🔗 Step 4: Preparing LangChain...")
            chain_start = time.time()
            if temperature is not None:
                logger.debug(f"   Creating custom LLM instance with temp={temp}")
                llm = ChatGroq(
                    api_key=settings.GROQ_API_KEY,
                    model_name=settings.GROQ_MODEL,
                    temperature=temp,
                    max_tokens=settings.MAX_TOKENS,
                )
                chain = self.prompt_template | llm | self.output_parser
            else:
                logger.debug("   Using default chain")
                chain = self.chain
            chain_time = time.time() - chain_start
            logger.info(f"✅ Chain ready in {chain_time*1000:.2f}ms")
            
            # Step 5: Invoke LLM
            logger.info(f"🤖 Step 5: Calling Groq API (model: {self.model})...")
            llm_start = time.time()
            response = chain.invoke({
                "user_prompt": user_prompt
            })
            llm_time = time.time() - llm_start
            response_length = len(response)
            logger.info(f"✅ LLM response received in {llm_time*1000:.2f}ms ({response_length} chars)")
            logger.debug(f"   Response preview: {response[:200]}...")
            
            # Step 6: Extract HTML
            logger.info("🔧 Step 6: Extracting and cleaning HTML...")
            extract_start = time.time()
            html_content = self._extract_html(response)
            extract_time = time.time() - extract_start
            logger.info(f"✅ HTML extracted in {extract_time*1000:.2f}ms")
            
            # Step 7: Validate HTML
            logger.info("✔️  Step 7: Validating HTML...")
            validate_start = time.time()
            html_lower = html_content.strip().lower()
            if not (html_lower.startswith('<!doctype') or 
                    html_lower.startswith('<html') or 
                    '<html' in html_lower[:100]):
                if '<' in html_content and '>' in html_content:
                    logger.warning("⚠️  DOCTYPE missing, adding it...")
                    if not html_lower.startswith('<!doctype'):
                        html_content = '<!DOCTYPE html>\n' + html_content
                else:
                    raise ValueError("Generated content is not valid HTML")
            validate_time = time.time() - validate_start
            logger.info(f"✅ HTML validated in {validate_time*1000:.2f}ms")
            
            # Step 8: Calculate metrics
            logger.info("📊 Step 8: Calculating metrics...")
            tokens_used = self._estimate_tokens(user_prompt + html_content)
            
            # Total time
            total_time = time.time() - start_time
            
            # Summary
            logger.info("=" * 60)
            logger.info("🎉 DASHBOARD GENERATION COMPLETE")
            logger.info("=" * 60)
            logger.info(f"⏱️  Total Time: {total_time*1000:.2f}ms ({total_time:.2f}s)")
            logger.info(f"   ├─ JSON Parsing: {parse_time*1000:.2f}ms")
            logger.info(f"   ├─ Prompt Building: {prompt_time*1000:.2f}ms")
            logger.info(f"   ├─ Chain Setup: {chain_time*1000:.2f}ms")
            logger.info(f"   ├─ LLM API Call: {llm_time*1000:.2f}ms ({(llm_time/total_time)*100:.1f}%)")
            logger.info(f"   ├─ HTML Extraction: {extract_time*1000:.2f}ms")
            logger.info(f"   └─ HTML Validation: {validate_time*1000:.2f}ms")
            logger.info(f"📈 Tokens: ~{tokens_used:,} tokens")
            logger.info(f"📄 Output Size: {len(html_content):,} chars")
            logger.info(f"🌡️  Temperature: {temp}")
            logger.info(f"🤖 Model: {self.model}")
            logger.info("=" * 60)
            
            return {
                'html': html_content,
                'tokens_used': tokens_used,
                'model': self.model,
                'temperature': temp,
                'latency': {
                    'total_ms': round(total_time * 1000, 2),
                    'parse_ms': round(parse_time * 1000, 2),
                    'prompt_ms': round(prompt_time * 1000, 2),
                    'chain_ms': round(chain_time * 1000, 2),
                    'llm_ms': round(llm_time * 1000, 2),
                    'extract_ms': round(extract_time * 1000, 2),
                    'validate_ms': round(validate_time * 1000, 2),
                }
            }
            
        except json.JSONDecodeError as e:
            logger.error(f"❌ JSON Parse Error: {str(e)}")
            raise ValueError(f"Invalid JSON data: {str(e)}")
        except Exception as e:
            logger.error(f"❌ Generation Error: {str(e)}")
            logger.exception("Full traceback:")
            raise Exception(f"Error generating dashboard: {str(e)}")
    
    def _extract_html(self, content: str) -> str:
        """
        Extract HTML from response, removing markdown code blocks if present
        
        Args:
            content: Raw content from LLM
            
        Returns:
            Clean HTML string
        """
        # Remove markdown code blocks if present
        # Pattern: ```html ... ``` or ``` ... ```
        pattern = r'```(?:html)?\s*(.*?)\s*```'
        match = re.search(pattern, content, re.DOTALL)
        
        if match:
            return match.group(1).strip()
        
        # If no code blocks found, return as is
        return content.strip()
    
    def _estimate_tokens(self, text: str) -> int:
        """
        Rough estimation of tokens (4 chars ≈ 1 token)
        For accurate tracking, use LangChain callbacks
        
        Args:
            text: Text to estimate tokens for
            
        Returns:
            Estimated token count
        """
        return len(text) // 4
    
    def test_connection(self) -> bool:
        """
        Test connection to Groq API using LangChain
        
        Returns:
            bool: True if connection successful
        """
        try:
            response = self.llm.invoke("Hello")
            return True
        except Exception:
            return False

# Create singleton instance
llm_service = LLMService()
