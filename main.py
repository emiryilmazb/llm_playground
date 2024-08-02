from models import get_openai_response, get_google_response
from flask import Flask, request, jsonify, redirect
from flask_swagger_ui import get_swaggerui_blueprint


app = Flask(__name__)

def send_to_all_models(prompt):
    responses = {}
    
    # OpenAI model
    try:
        responses['OpenAI'] = get_openai_response(prompt)
    except Exception as e:
        responses['OpenAI'] = f"Error: {str(e)}"
    
    # Google model
    try:
        responses['Google'] = get_google_response(prompt)
    except Exception as e:
        responses['Google'] = f"Error: {str(e)}"
    
    return responses

@app.route('/api/get_responses', methods=['POST'])
def get_responses():
    data = request.json
    prompt = data.get('prompt', '')
    results = send_to_all_models(prompt)
    return jsonify(results)




@app.route('/')
def redirect_to_docs():
    return redirect('/docs')




SWAGGER_UI_SCRIPT = "https://cdn.jsdelivr.net/npm/swagger-ui-dist@latest/swagger-ui-bundle.js"
SWAGGER_UI_STYLE = "https://cdn.jsdelivr.net/npm/swagger-ui-dist@latest/swagger-ui.css"

swaggerui_blueprint = get_swaggerui_blueprint(
    '/docs',
    '/static/swagger.json',
    config={
        'app_name': "My Application"
    }
)

app.register_blueprint(swaggerui_blueprint)

if __name__ == "__main__":
    app.run(debug=True)