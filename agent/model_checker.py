"""
OpenAI model compatibility checker and updater.
Ensures we're using the latest available models.
"""

import openai
import os
from typing import List, Dict, Any

class ModelChecker:
    def __init__(self):
        api_key = os.getenv('OPENAI_API_KEY')
        
        if api_key and api_key != 'your_openai_api_key_here':
            self.client = openai.OpenAI(api_key=api_key)
            self.has_api_key = True
        else:
            self.client = None
            self.has_api_key = False
        
        # Current recommended models (as of 2024)
        self.recommended_models = {
            'vision': 'gpt-4o',           # GPT-4o has built-in vision
            'text': 'gpt-4o',             # GPT-4o for text generation
            'fallback_vision': 'gpt-4o-mini',  # Cheaper alternative
            'fallback_text': 'gpt-4o-mini'     # Cheaper alternative
        }
        
        # Deprecated models to avoid
        self.deprecated_models = [
            'gpt-4-vision-preview',
            'gpt-4-1106-vision-preview',
            'gpt-4-0125-preview'
        ]
    
    def check_model_availability(self) -> Dict[str, Any]:
        """Check which models are available and recommend the best ones."""
        if not self.has_api_key:
            return {
                'status': 'no_api_key',
                'error': 'No valid OpenAI API key found',
                'recommended': self.recommended_models
            }
        
        try:
            # Get list of available models
            models_response = self.client.models.list()
            available_models = [model.id for model in models_response.data]
            
            result = {
                'available_models': available_models,
                'recommended': {},
                'deprecated_found': [],
                'status': 'success'
            }
            
            # Check recommended models
            for purpose, model_name in self.recommended_models.items():
                if model_name in available_models:
                    result['recommended'][purpose] = model_name
                else:
                    result['recommended'][purpose] = None
            
            # Check for deprecated models
            for deprecated in self.deprecated_models:
                if deprecated in available_models:
                    result['deprecated_found'].append(deprecated)
            
            return result
            
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e),
                'recommended': self.recommended_models  # Return defaults
            }
    
    def get_best_models(self) -> Dict[str, str]:
        """Get the best available models for vision and text generation."""
        check_result = self.check_model_availability()
        
        if check_result['status'] in ['error', 'no_api_key']:
            if check_result['status'] == 'no_api_key':
                print("⚠️  No valid OpenAI API key found")
            else:
                print(f"⚠️  Could not check model availability: {check_result['error']}")
            print("🔄 Using default recommended models")
            return {
                'vision': self.recommended_models['vision'],
                'text': self.recommended_models['text']
            }
        
        best_models = {}
        
        # Choose best vision model
        if check_result['recommended']['vision']:
            best_models['vision'] = check_result['recommended']['vision']
        elif check_result['recommended']['fallback_vision']:
            best_models['vision'] = check_result['recommended']['fallback_vision']
        else:
            best_models['vision'] = 'gpt-4o'  # Default fallback
        
        # Choose best text model
        if check_result['recommended']['text']:
            best_models['text'] = check_result['recommended']['text']
        elif check_result['recommended']['fallback_text']:
            best_models['text'] = check_result['recommended']['fallback_text']
        else:
            best_models['text'] = 'gpt-4o'  # Default fallback
        
        return best_models
    
    def print_model_status(self):
        """Print current model status and recommendations."""
        print("🤖 Checking OpenAI Model Compatibility...")
        
        check_result = self.check_model_availability()
        
        if check_result['status'] == 'error':
            print(f"❌ Error checking models: {check_result['error']}")
            return
        
        print("✅ Model compatibility check complete")
        
        # Show recommended models
        print("\n📋 Recommended Models:")
        for purpose, model in check_result['recommended'].items():
            if model:
                print(f"   {purpose}: ✅ {model}")
            else:
                print(f"   {purpose}: ❌ Not available")
        
        # Show deprecated models if found
        if check_result['deprecated_found']:
            print("\n⚠️  Deprecated Models Found:")
            for deprecated in check_result['deprecated_found']:
                print(f"   ❌ {deprecated} (should be updated)")
        
        # Show current selection
        best_models = self.get_best_models()
        print(f"\n🎯 Selected Models:")
        print(f"   Vision: {best_models['vision']}")
        print(f"   Text: {best_models['text']}")
    
    def test_model_access(self, model_name: str) -> bool:
        """Test if we can access a specific model."""
        if not self.has_api_key:
            print(f"⚠️  Cannot test {model_name}: No API key")
            return False
            
        try:
            response = self.client.chat.completions.create(
                model=model_name,
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=5
            )
            return True
        except Exception as e:
            print(f"❌ Cannot access {model_name}: {e}")
            return False

def update_orchestrator_models():
    """Update the orchestrator with the best available models."""
    checker = ModelChecker()
    best_models = checker.get_best_models()
    
    print(f"🔄 Updating to use: Vision={best_models['vision']}, Text={best_models['text']}")
    
    return best_models

if __name__ == "__main__":
    # Test the model checker
    checker = ModelChecker()
    checker.print_model_status()
    
    # Test access to recommended models
    best_models = checker.get_best_models()
    print(f"\n🧪 Testing Model Access:")
    
    for purpose, model in best_models.items():
        if checker.test_model_access(model):
            print(f"   ✅ {model} - Access confirmed")
        else:
            print(f"   ❌ {model} - Access failed")
