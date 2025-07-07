from flask import Flask, render_template, request
from analysis import load_data, analyze_sleep, create_plot, get_recommendations
import matplotlib
matplotlib.use('Agg')  # Set non-interactive backend

app = Flask(__name__)

# Load data once when app starts
df = load_data()

@app.route('/')
def index():
    analysis_results = analyze_sleep(df)
    plot_data = create_plot(df)
    return render_template('index.html', 
                        analysis=analysis_results,
                        plot=plot_data)

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        age = int(request.form['age'])
        occupation = request.form['occupation']
        sleep_duration = float(request.form['sleep_duration'])
        sleep_quality = float(request.form['sleep_quality'])
        
        recommendations = get_recommendations(
            age, occupation, sleep_duration, sleep_quality
        )
        
        return render_template('index.html',
                            analysis=analyze_sleep(df),
                            plot=create_plot(df),
                            recommendations=recommendations,
                            user_data=request.form)
    except Exception as e:
        return render_template('index.html',
                            analysis=analyze_sleep(df),
                            plot=create_plot(df),
                            error=str(e))

if __name__ == '__main__':
    app.run(debug=True)