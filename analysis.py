import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import base64

def load_data():
    """Load and preprocess data"""
    df = pd.read_csv('data/Sleep_health_and_lifestyle_dataset.csv')
    
    # Data cleaning
    df['Sleep Duration'] = pd.to_numeric(df['Sleep Duration'], errors='coerce')
    df['Quality of Sleep'] = pd.to_numeric(df['Quality of Sleep'], errors='coerce')
    df['BMI Category'] = df['BMI Category'].replace({'Normal Weight': 'Normal'})
    
    # Extract blood pressure components
    df['Systolic BP'] = df['Blood Pressure'].apply(lambda x: int(x.split('/')[0]))
    df['Diastolic BP'] = df['Blood Pressure'].apply(lambda x: int(x.split('/')[1]))
    
    return df

def analyze_sleep(df):
    """Calculate key metrics"""
    analysis = {
        'avg_sleep': round(df['Quality of Sleep'].mean(), 2),
        'avg_duration': round(df['Sleep Duration'].mean(), 2),
        'avg_physical_activity': round(df['Physical Activity Level'].mean(), 2),
        'sleep_by_occupation': df.groupby('Occupation')['Quality of Sleep']
                               .mean().sort_values(ascending=False).to_dict(),
        'sleep_disorders': df['Sleep Disorder'].value_counts().to_dict()
    }
    return analysis

def create_plot(df):
    """Generate sleep duration by age plot"""
    try:
        plt.close('all')
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Group by age and calculate mean sleep duration
        sleep_by_age = df.groupby('Age')['Sleep Duration'].mean()
        sleep_by_age.plot(kind='bar', color='skyblue', ax=ax)
        
        ax.set_title('Average Sleep Duration by Age')
        ax.set_xlabel('Age')
        ax.set_ylabel('Hours of Sleep')
        fig.tight_layout()
        
        # Convert plot to base64
        buffer = BytesIO()
        fig.savefig(buffer, format='png', dpi=100)
        plt.close(fig)
        return base64.b64encode(buffer.getvalue()).decode('utf-8')
    except Exception as e:
        print(f"Plot generation error: {str(e)}")
        return None

def get_recommendations(age, occupation, sleep_duration, quality):
    """Generate personalized recommendations"""
    recommendations = []
    
    if sleep_duration < 7:
        recommendations.append("Aim for 7-9 hours of sleep nightly.")
    elif sleep_duration > 9:
        recommendations.append("Consider reducing sleep to 7-9 hours.")
    
    if quality < 5:
        recommendations.append("Improve sleep quality with a consistent schedule.")
        recommendations.append("Reduce screen time before bedtime.")
    
    if occupation in ['Doctor', 'Nurse', 'Engineer']:
        recommendations.append(f"As a {occupation}, consider short power naps.")
    
    if age > 50:
        recommendations.append("Try a slightly cooler bedroom temperature.")
    
    return recommendations if recommendations else ["Your sleep habits look good!"]