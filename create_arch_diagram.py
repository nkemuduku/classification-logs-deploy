import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

fig, ax = plt.subplots(1, 1, figsize=(14, 10))
ax.set_xlim(0, 10)
ax.set_ylim(0, 12)
ax.axis('off')

# Title
ax.text(5, 11.5, 'Log Classification Pipeline Architecture', 
        fontsize=18, fontweight='bold', ha='center')

# Colors
input_color = '#E8F4F8'
process_color = '#FFE8CC'
classifier_color = '#E8F8E8'
output_color = '#F0E8F8'
arrow_color = '#333333'

# Helper function to draw boxes
def draw_box(ax, x, y, width, height, text, color, fontsize=11):
    box = FancyBboxPatch((x - width/2, y - height/2), width, height,
                          boxstyle="round,pad=0.1", 
                          edgecolor='black', facecolor=color, linewidth=2)
    ax.add_patch(box)
    ax.text(x, y, text, ha='center', va='center', fontsize=fontsize, fontweight='bold')

# Helper function to draw arrows
def draw_arrow(ax, x1, y1, x2, y2, label=''):
    arrow = FancyArrowPatch((x1, y1), (x2, y2),
                           arrowstyle='->', mutation_scale=25, 
                           linewidth=2.5, color=arrow_color)
    ax.add_patch(arrow)
    if label:
        mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
        ax.text(mid_x + 0.3, mid_y, label, fontsize=9, style='italic', 
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

# Input Layer
draw_box(ax, 5, 10, 2, 0.8, 'CSV Input\n(source, log_message)', input_color, fontsize=10)

# Arrow to classifier
draw_arrow(ax, 5, 9.6, 5, 9)

# Main Orchestrator
draw_box(ax, 5, 8.3, 3, 0.8, 'classify.py - Main Orchestrator', process_color, fontsize=11)

# Arrow down to decision
draw_arrow(ax, 5, 7.9, 5, 7.3)

# Decision: Is source LegacyCRM?
draw_box(ax, 5, 6.8, 2.5, 0.8, 'Is source\nLegacyCRM?', '#FFF8DC', fontsize=10)

# Left path: No -> Regex first
draw_arrow(ax, 3.75, 6.8, 2.5, 5.8, 'No')
draw_box(ax, 2.5, 5.3, 2, 0.8, 'Regex Classifier\n(processor_regex.py)', classifier_color, fontsize=9)

# Regex match decision
draw_arrow(ax, 2.5, 4.9, 2.5, 4.3)
draw_box(ax, 2.5, 3.8, 2, 0.8, 'Match\nFound?', '#FFF8DC', fontsize=9)

# Regex match -> output
draw_arrow(ax, 1.5, 3.8, 0.8, 3.8, 'Yes')
draw_box(ax, 0.3, 3.8, 0.6, 0.8, 'Label', output_color, fontsize=9)

# No match -> BERT
draw_arrow(ax, 2.5, 3.4, 2.5, 2.6, 'No')
draw_box(ax, 2.5, 2.1, 2, 0.8, 'BERT Classifier\n(processor_bert.py)', classifier_color, fontsize=9)

# BERT confidence check
draw_arrow(ax, 2.5, 1.7, 2.5, 1.1)
draw_box(ax, 2.5, 0.6, 2, 0.8, 'Confidence\n≥ 0.5?', '#FFF8DC', fontsize=9)

# High confidence -> label
draw_arrow(ax, 1.5, 0.6, 0.8, 0.6, 'Yes')
draw_box(ax, 0.3, 0.6, 0.6, 0.8, 'Label', output_color, fontsize=9)

# Low confidence -> Unclassified
draw_arrow(ax, 3.5, 0.6, 4.2, 0.6, 'No')
draw_box(ax, 4.8, 0.6, 1, 0.8, 'Unclassified', output_color, fontsize=9)

# Right path: Yes -> LLM
draw_arrow(ax, 6.25, 6.8, 7.5, 5.8, 'Yes')
draw_box(ax, 7.5, 5.3, 2, 0.8, 'LLM Classifier\n(processor_llm.py)', classifier_color, fontsize=9)

# LLM output
draw_arrow(ax, 7.5, 4.9, 7.5, 4.1)
draw_box(ax, 7.5, 3.6, 2, 0.8, 'LLM Response\n(Groq API)', '#FFF8DC', fontsize=9)

# LLM -> Label
draw_arrow(ax, 7.5, 3.2, 7.5, 0.6)
draw_box(ax, 7.5, 0.6, 0.6, 0.8, 'Label', output_color, fontsize=9)

# Final output aggregation
draw_arrow(ax, 0.8, 3.4, 4.5, 1.2)
draw_arrow(ax, 0.8, 0.6, 4.5, 1.2)
draw_arrow(ax, 4.8, 0.6, 4.5, 1.2)
draw_arrow(ax, 7.5, 0.2, 4.5, 1.2)

# Output
draw_box(ax, 5, -0.5, 3, 0.9, 'CSV Output\n(with target_label)', output_color, fontsize=11)

# Legend
legend_y = 11
ax.text(0.3, legend_y - 0.2, 'Input Data', fontsize=9, color='white', 
        bbox=dict(boxstyle='round', facecolor='#336699', alpha=0.7))
ax.text(0.3, legend_y - 0.8, 'Processing', fontsize=9, color='white',
        bbox=dict(boxstyle='round', facecolor='#CC8833', alpha=0.7))
ax.text(0.3, legend_y - 1.4, 'Classification', fontsize=9, color='white',
        bbox=dict(boxstyle='round', facecolor='#339933', alpha=0.7))
ax.text(0.3, legend_y - 2.0, 'Decision', fontsize=9, color='white',
        bbox=dict(boxstyle='round', facecolor='#CCCC00', alpha=0.7))
ax.text(0.3, legend_y - 2.6, 'Output', fontsize=9, color='white',
        bbox=dict(boxstyle='round', facecolor='#9933CC', alpha=0.7))

plt.tight_layout()
plt.savefig(r'resources\arch.png', dpi=300, bbox_inches='tight', facecolor='white')
print('[OK] Architecture diagram saved to resources/arch.png')
