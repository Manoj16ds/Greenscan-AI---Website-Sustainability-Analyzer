# visualizer.py
import matplotlib.pyplot as plt

def plot_image_classification(classification, output_path="classification_pie.png"):
    labels = ['Essential Images', 'Decorative Images']
    sizes = [len(classification['essential']), len(classification['decorative'])]
    colors = ['#4CAF50', '#FF7043']
    
    plt.figure(figsize=(5,5))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=140)
    plt.title("Image Classification")
    plt.axis('equal')
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

def plot_carbon_vs_size(page_size_kb, carbon_kg, output_path="carbon_vs_size.png"):
    labels = ['Page Size (KB)', 'CO2 Emission (kg/month)']
    values = [page_size_kb, carbon_kg]
    colors = ['#42A5F5', '#66BB6A']
    
    plt.figure(figsize=(5,4))
    plt.bar(labels, values, color=colors)
    plt.title("Page Size vs CO2 Emission")
    plt.ylabel("Value")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    
def plot_emission_comparison(original_carbon, optimized_carbon, output_path="emission_comparison.png"):
    labels = ['Original Emission', 'Optimized Emission']
    values = [original_carbon, optimized_carbon]
    colors = ['#EF5350', '#66BB6A']

    plt.figure(figsize=(5,4))
    plt.bar(labels, values, color=colors)
    plt.title("CO2 Emissions: Before vs After Optimization")
    plt.ylabel("kg/month")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
