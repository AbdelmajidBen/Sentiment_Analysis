from django.shortcuts import render
from pymongo import MongoClient
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Tweet
import matplotlib.pyplot as plt
from io import BytesIO
from pymongo import MongoClient
import base64
from collections import Counter
import numpy as np

def say_hello(request):
    return render(request, 'hello.html')

def dashboard(request):
    tweets = Tweet.objects.all()
    # Extract timestamp and prediction from each tweet
    timestamps = []
    predictions = []
    confidence = []  # New list to store maximum predictions
    
    cpu_usages = []  # List to store CPU usage
    memory_usages = []  # List to store memory usage

    for tweet in tweets:
        timestamps.append(tweet.timestamp)
        predictions.append(tweet.prediction)
        
        # Assuming tweet.rawPredictionArray is the array of predictions
        
        confidence.append(max(tweet.rawPredictionArray))
        cpu_usages.append(tweet.cpu_usage)
        memory_usages.append(tweet.memory_usage)
        
    

    # Create the pie chart for predictions
    prediction_counts = Counter(predictions)
    labels = [str(pred) for pred in prediction_counts.keys()]
    sizes = list(prediction_counts.values())

    plt.figure(figsize=(4, 4))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%')
    plt.title('Predictions Distribution')
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle

    # Convert the pie chart plot to a bytes object
    pie_buffer = BytesIO()
    plt.savefig(pie_buffer, format='png')
    pie_buffer.seek(0)
    pie_image_png = pie_buffer.getvalue()
    plt.close()

    # Encode the pie chart as a base64 string
    pie_graphic = base64.b64encode(pie_image_png)
    pie_graphic = pie_graphic.decode('utf-8')

    # Create the histogram plot for number of predictions at each timestamp
    plt.figure(figsize=(7, 4))
    plt.hist(timestamps, bins=50, color='blue', alpha=0.7)
    plt.xlabel('Timestamp')
    plt.ylabel('Number of Predictions')
    plt.title('Number of Predictions over Time')

    # Convert the histogram plot to a bytes object
    plot_buffer = BytesIO()
    plt.savefig(plot_buffer, format='png')
    plot_buffer.seek(0)
    plot_image_png = plot_buffer.getvalue()
    plt.close()

    # Encode the histogram plot as a base64 string
    plot_graphic = base64.b64encode(plot_image_png)
    plot_graphic = plot_graphic.decode('utf-8')
    
    # Create the line plot for maximum predictions over time
    plt.figure(figsize=(7, 4))
    plt.plot(timestamps[-100:], confidence[-100:], color='red', marker='o', linestyle='-')
    plt.xlabel('Timestamp')

    plt.ylabel('Confidence')
    plt.title('Maximum Prediction over Time')

    # Convert the line plot to a bytes object
    line_buffer = BytesIO()
    plt.savefig(line_buffer, format='png')
    line_buffer.seek(0)
    line_image_png = line_buffer.getvalue()
    plt.close()

    # Encode the line plot as a base64 string
    line_graphic = base64.b64encode(line_image_png)
    line_graphic = line_graphic.decode('utf-8')
    
    
    # Create the line plot for CPU and memory usage over time
    plt.figure(figsize=(10, 6))
    plt.plot(timestamps[-100:], cpu_usages[-100:], color='blue', marker='o', linestyle='-', label='CPU Usage')
    plt.plot(timestamps[-100:], memory_usages[-100:], color='green', marker='o', linestyle='-', label='Memory Usage')
    plt.xlabel('Timestamp')
    plt.ylabel('Usage (%)')
    plt.title('CPU and Memory Usage over Time')
    plt.legend()

    # Convert the line plot to a bytes object
    cpu_memory_usage_buffer = BytesIO()
    plt.savefig(cpu_memory_usage_buffer, format='png')
    cpu_memory_usage_buffer.seek(0)
    cpu_memory_usage_png = cpu_memory_usage_buffer.getvalue()
    plt.close()

    # Encode the line plot as a base64 string
    cpu_memory_graphic = base64.b64encode(cpu_memory_usage_png)
    cpu_memory_graphic = cpu_memory_graphic.decode('utf-8')

    # Pass the base64 strings of all plots to the template
    return render(request, 'dashboard.html', {'pie_graphic': pie_graphic, 'plot_graphic': plot_graphic, 'line_graphic': line_graphic, "cpu_memory_graphic":cpu_memory_graphic})

def architecture(request):
    return render(request, 'architecture.html')

def data(request):
    tweets_list = Tweet.objects.all()
    tweets_per_page = 20
    paginator = Paginator(tweets_list, tweets_per_page)
    page_number = request.GET.get('page', 1)
    try:
        tweets = paginator.page(page_number)
    except PageNotAnInteger:
        tweets = paginator.page(1)
    except EmptyPage:
        tweets = paginator.page(paginator.num_pages)
    return render(request, 'data.html', {'tweets': tweets})

def testing(request):
    return render(request, 'testing.html')

def models(request):
    return render(request, 'models.html')

def team(request):
    return render(request, 'team.html')
