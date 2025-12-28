"""
Generate FinGuard AI Thumbnail Card
Creates a professional project thumbnail for Kaggle submission
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Circle
import numpy as np

fig = plt.figure(figsize=(12, 7), dpi=150)
ax = fig.add_subplot(111)
ax.set_xlim(0, 12)
ax.set_ylim(0, 7)
ax.axis('off')

# Background gradient effect with rounded rectangle
background = FancyBboxPatch((0.2, 0.2), 11.6, 6.6, boxstyle="round,pad=0.2",
                            edgecolor='none', facecolor='#0f172a', linewidth=0)
ax.add_patch(background)

# Top accent bar (teal)
accent_bar = FancyBboxPatch((0.2, 5.8), 11.6, 1, boxstyle="round,pad=0.1",
                            edgecolor='none', facecolor='#0d9488', linewidth=0)
ax.add_patch(accent_bar)

# Main title
ax.text(6, 6.4, 'FinGuard AI', fontsize=48, ha='center', va='center',
        fontweight='bold', color='white', family='sans-serif')

# Subtitle
ax.text(6, 5.9, 'Multi-Agent Personal Finance Concierge', fontsize=16, ha='center', va='center',
        color='#ccfbf1', style='italic', family='sans-serif')

# Indian context indicator
ax.text(1.5, 5.2, '🇮🇳', fontsize=28, ha='center', va='center')
ax.text(1.5, 4.6, 'For India', fontsize=11, ha='center', va='center',
        color='white', fontweight='bold')

# ADK badge
adk_badge = FancyBboxPatch((4, 4.7), 1.8, 0.6, boxstyle="round,pad=0.05",
                           edgecolor='#fbbf24', facecolor='#fef08a', linewidth=2)
ax.add_patch(adk_badge)
ax.text(4.9, 5, 'Google ADK', fontsize=10, ha='center', va='center',
        fontweight='bold', color='#92400e')

# MCP badge
mcp_badge = FancyBboxPatch((6.2, 4.7), 1.8, 0.6, boxstyle="round,pad=0.05",
                           edgecolor='#06b6d4', facecolor='#cffafe', linewidth=2)
ax.add_patch(mcp_badge)
ax.text(7.1, 5, 'MCP Tools', fontsize=10, ha='center', va='center',
        fontweight='bold', color='#164e63')

# Features badge
features_badge = FancyBboxPatch((8.4, 4.7), 2.4, 0.6, boxstyle="round,pad=0.05",
                                edgecolor='#10b981', facecolor='#d1fae5', linewidth=2)
ax.add_patch(features_badge)
ax.text(9.6, 5, '11/15 Features', fontsize=10, ha='center', va='center',
        fontweight='bold', color='#065f46')

# Main content box
content_box = FancyBboxPatch((0.5, 0.8), 11, 3.6, boxstyle="round,pad=0.15",
                             edgecolor='#06b6d4', facecolor='#f0f9ff', linewidth=2)
ax.add_patch(content_box)

# Feature items with icons
features_list = [
    ('📊', 'Transaction Analysis', 'CSV parsing + ₹ breakdown'),
    ('🤖', 'Multi-Agent Orchestration', 'A2A delegation • Session state'),
    ('💰', '50-30-20 Budget Plan', 'Indian financial context'),
    ('🔧', 'MCP Tool Server', '3 financial calculation tools'),
]

y_pos = 4
for icon, title, desc in features_list:
    ax.text(1, y_pos, icon, fontsize=20, ha='left', va='center')
    ax.text(1.8, y_pos + 0.15, title, fontsize=11, ha='left', va='center',
           fontweight='bold', color='#0f172a')
    ax.text(1.8, y_pos - 0.25, desc, fontsize=9, ha='left', va='center',
           color='#475569', style='italic')
    y_pos -= 0.85

# Bottom section
# GitHub link
ax.text(2.5, 0.4, '📍 github.com/adityait019/finguard-ai',
       fontsize=10, ha='left', va='center', color='#0d9488', fontweight='bold')

# Kaggle badge
kaggle_badge = FancyBboxPatch((8.5, 0.15), 2.8, 0.5, boxstyle="round,pad=0.08",
                             edgecolor='#dc2626', facecolor='#fee2e2', linewidth=2)
ax.add_patch(kaggle_badge)
ax.text(9.9, 0.4, 'Kaggle Capstone 2025', fontsize=10, ha='center', va='center',
       fontweight='bold', color='#7f1d1d')

plt.tight_layout()
plt.savefig('finguard_thumbnail_card.png', dpi=300, bbox_inches='tight', 
           facecolor='white', edgecolor='none')
print("✓ Saved: finguard_thumbnail_card.png")
print("\nUse this thumbnail for:")
print("  - Kaggle project card")
print("  - GitHub repo header")
print("  - LinkedIn post preview")
print("  - Presentation slide")
plt.show()
