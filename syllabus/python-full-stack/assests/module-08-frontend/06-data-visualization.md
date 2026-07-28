# Data Visualization in the Browser

**Module 08 — Front-End for Python Developers | Topic 6**

---

## Why Visualize Data?

Imagine Priya is a trainer at TechPath Institute, Bhopal. She has a spreadsheet with 500 rows of student marks. She could stare at those numbers for an hour, or she could look at a single bar chart and instantly see that Module 04 (Database Design) had the lowest scores. Charts tell stories that tables cannot.

**Data visualization turns numbers into pictures.** Our brains process images 60,000 times faster than text. A well-made chart can:

- Reveal patterns (scores dropping every Monday)
- Compare values (which city has the most enrollments)
- Show trends (course completions rising month by month)
- Highlight outliers (one student scoring 100% while others average 60%)

In this topic, you will learn to create interactive charts in the browser using **Chart.js** and **Plotly.js**, and load real data from a Python API.

---

## Chart.js Basics

Chart.js is a free, open-source JavaScript library for creating beautiful charts. It is simple enough for beginners yet powerful enough for production dashboards.

### Setting Up Chart.js

Add Chart.js via CDN in your HTML file:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Student Performance Dashboard — TechPath Institute</title>
    <style>
        .chart-container {
            width: 100%;
            max-width: 600px;
            margin: 20px auto;
        }
    </style>
</head>
<body>
    <h1>Student Performance Dashboard</h1>

    <div class="chart-container">
        <canvas id="marksChart"></canvas>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/chart.js@4"></script>
    <script src="dashboard.js"></script>
</body>
</html>
```

**Important:** Chart.js uses the `<canvas>` element — you must create a `<canvas>` tag and give it an `id`.

### Your First Chart — Bar Chart (Student Marks)

Rahul scored the following marks across five modules:

```javascript
// dashboard.js
const ctx = document.getElementById("marksChart").getContext("2d");

const marksChart = new Chart(ctx, {
    type: "bar",
    data: {
        labels: ["Python Core", "OOP", "Web Basics", "Database", "FastAPI"],
        datasets: [{
            label: "Rahul's Marks (out of 100)",
            data: [85, 72, 90, 65, 78],
            backgroundColor: [
                "#4CAF50",  // green
                "#2196F3",  // blue
                "#FF9800",  // orange
                "#F44336",  // red (lowest)
                "#9C27B0"   // purple
            ],
            borderWidth: 1
        }]
    },
    options: {
        responsive: true,
        scales: {
            y: {
                beginAtZero: true,
                max: 100
            }
        }
    }
});
```

This creates a bar chart where each bar represents a module. Rahul can immediately see his weakest subject is Database (65 marks) — shown in red.

### Chart Types Available in Chart.js

| Chart Type | Best For | Example Use |
|-----------|----------|-------------|
| `bar` | Comparing categories | Marks by module |
| `line` | Showing trends over time | Attendance over 12 weeks |
| `pie` | Showing proportions | Pass vs fail ratio |
| `doughnut` | Proportions (with center space) | Course completion percentage |
| `radar` | Multi-dimensional comparison | Skill assessment |
| `scatter` | Relationship between two values | Study hours vs marks |
| `polarArea` | Proportions with magnitude | Topic difficulty ratings |

### Line Chart — Attendance Over Time

Sneha wants to track her attendance across 10 weeks:

```javascript
const attendanceChart = new Chart(
    document.getElementById("attendanceChart").getContext("2d"),
    {
        type: "line",
        data: {
            labels: ["Week 1", "Week 2", "Week 3", "Week 4", "Week 5",
                     "Week 6", "Week 7", "Week 8", "Week 9", "Week 10"],
            datasets: [{
                label: "Classes Attended (out of 5)",
                data: [5, 4, 5, 3, 5, 5, 4, 5, 5, 4],
                borderColor: "#2196F3",
                backgroundColor: "rgba(33, 150, 243, 0.1)",
                fill: true,          // Fill area under line
                tension: 0.3         // Smooth the line slightly
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: { beginAtZero: true, max: 5 }
            }
        }
    }
);
```

### Pie Chart — Pass/Fail Ratio

Amit wants to show what percentage of students passed Module 04:

```javascript
const passFailChart = new Chart(
    document.getElementById("passFailChart").getContext("2d"),
    {
        type: "pie",
        data: {
            labels: ["Passed", "Failed"],
            datasets: [{
                data: [38, 12],
                backgroundColor: ["#4CAF50", "#F44336"]
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: "Module 04 — Pass/Fail Ratio (50 Students)"
                }
            }
        }
    }
);
```

### Doughnut Chart — Course Completion

```javascript
const completionChart = new Chart(
    document.getElementById("completionChart").getContext("2d"),
    {
        type: "doughnut",
        data: {
            labels: ["Completed", "In Progress", "Not Started"],
            datasets: [{
                data: [60, 25, 15],
                backgroundColor: ["#4CAF50", "#FF9800", "#9E9E9E"]
            }]
        }
    }
);
```

---

## Customizing Charts

### Colors, Labels, Legends, and Tooltips

Chart.js gives you full control over how your chart looks:

```javascript
const customChart = new Chart(ctx, {
    type: "bar",
    data: { /* ... */ },
    options: {
        responsive: true,
        plugins: {
            // Chart title
            title: {
                display: true,
                text: "Batch 2026 — Module-wise Average Marks",
                font: { size: 18 }
            },
            // Legend (the colored squares with labels)
            legend: {
                position: "bottom",    // top, bottom, left, right
                labels: {
                    font: { size: 14 },
                    padding: 20
                }
            },
            // Tooltip (popup on hover)
            tooltip: {
                backgroundColor: "#333",
                titleFont: { size: 14 },
                bodyFont: { size: 13 },
                callbacks: {
                    label: function(context) {
                        return context.dataset.label + ": " +
                               context.parsed.y + " marks";
                    }
                }
            }
        },
        scales: {
            y: {
                beginAtZero: true,
                title: {
                    display: true,
                    text: "Marks (out of 100)"
                }
            },
            x: {
                title: {
                    display: true,
                    text: "Modules"
                }
            }
        }
    }
});
```

### Common Customization Options

| What to Change | Property | Example Value |
|---------------|----------|---------------|
| Chart title | `plugins.title.text` | `"Student Dashboard"` |
| Title size | `plugins.title.font.size` | `18` |
| Legend position | `plugins.legend.position` | `"bottom"` |
| Y-axis label | `scales.y.title.text` | `"Marks"` |
| Start Y from zero | `scales.y.beginAtZero` | `true` |
| Bar border radius | `borderRadius` in dataset | `5` |
| Line smoothness | `tension` in dataset | `0.3` (0 = sharp, 1 = very smooth) |
| Fill under line | `fill` in dataset | `true` |

---

## Plotly.js for Interactive Charts

Chart.js is great for simple charts. But when you need zoom, pan, hover details, and export to image — **Plotly.js** is the better choice.

### Setting Up Plotly.js

```html
<script src="https://cdn.plot.ly/plotly-2.35.0.min.js"></script>

<div id="interactiveChart"></div>
```

### Interactive Bar Chart with Plotly

```javascript
const moduleNames = [
    "Python Core", "OOP", "Web Basics",
    "Database", "FastAPI", "Django", "Frontend"
];
const avgMarks = [78, 72, 85, 65, 80, 74, 88];

Plotly.newPlot("interactiveChart", [{
    x: moduleNames,
    y: avgMarks,
    type: "bar",
    marker: {
        color: avgMarks.map(m => m >= 75 ? "#4CAF50" : "#F44336")
    },
    text: avgMarks.map(m => m + " marks"),
    textposition: "outside"
}], {
    title: "Batch 2026 — Average Marks by Module",
    yaxis: { title: "Average Marks", range: [0, 100] },
    xaxis: { title: "Module" }
});
```

With Plotly, students can **hover** over bars to see exact values, **zoom** into specific modules, and even **download the chart as a PNG** — all built in, no extra code needed.

### Chart.js vs Plotly.js

| Feature | Chart.js | Plotly.js |
|---------|----------|-----------|
| File size | ~70 KB | ~3.5 MB |
| Learning curve | Simple | Moderate |
| Interactivity | Basic (hover tooltips) | Advanced (zoom, pan, export) |
| Chart types | 8 built-in | 40+ including 3D, maps |
| Best for | Dashboards, reports | Data exploration, scientific |
| Animation | Yes | Yes |
| Export to image | With plugin | Built-in |

**Rule of thumb:** Use Chart.js for dashboards where you control the data. Use Plotly.js when users need to explore data themselves.

---

## Loading Data from a Python API

In a real application, your chart data comes from the backend — not hardcoded in JavaScript. Here is how to load data from a FastAPI endpoint.

### The FastAPI Endpoint

```python
# app/api/v1/endpoints/analytics.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/analytics/module-marks")
async def get_module_marks():
    # In production, this would query the database
    return {
        "success": True,
        "data": {
            "labels": ["Python Core", "OOP", "Web Basics",
                       "Database", "FastAPI", "Django", "Frontend"],
            "marks": [78, 72, 85, 65, 80, 74, 88],
            "attendance": [92, 88, 95, 80, 90, 85, 93]
        }
    }
```

### Fetching and Rendering the Chart

```javascript
// dashboard.js
async function loadDashboard() {
    try {
        const response = await fetch("/api/v1/analytics/module-marks");
        const result = await response.json();

        if (!result.success) {
            console.error("API error:", result);
            return;
        }

        const { labels, marks, attendance } = result.data;

        // Create a chart with two datasets
        new Chart(document.getElementById("dashboardChart").getContext("2d"), {
            type: "bar",
            data: {
                labels: labels,
                datasets: [
                    {
                        label: "Average Marks (%)",
                        data: marks,
                        backgroundColor: "#2196F3"
                    },
                    {
                        label: "Attendance (%)",
                        data: attendance,
                        backgroundColor: "#4CAF50"
                    }
                ]
            },
            options: {
                responsive: true,
                plugins: {
                    title: {
                        display: true,
                        text: "TechPath Batch 2026 — Performance Overview"
                    }
                },
                scales: {
                    y: { beginAtZero: true, max: 100 }
                }
            }
        });
    } catch (error) {
        console.error("Failed to load dashboard data:", error);
    }
}

// Load the dashboard when the page is ready
document.addEventListener("DOMContentLoaded", loadDashboard);
```

---

## Responsive Charts

Charts must look good on both Ananya's laptop and Amit's phone. Chart.js handles this well if you set it up correctly.

### Making Charts Responsive

```html
<!-- Wrap canvas in a container with max-width -->
<div style="width: 100%; max-width: 700px; margin: 0 auto;">
    <canvas id="myChart"></canvas>
</div>
```

```javascript
new Chart(ctx, {
    type: "bar",
    data: { /* ... */ },
    options: {
        responsive: true,           // Resize with container
        maintainAspectRatio: true,   // Keep width/height ratio
        aspectRatio: 2               // Width = 2x height
    }
});
```

| Screen Size | Tip |
|-------------|-----|
| Desktop (1200px+) | Show full labels, full legend |
| Tablet (768px) | Shorter labels, legend at bottom |
| Mobile (375px) | Consider `aspectRatio: 1` (square chart) |

---

## Dashboard Layout with Multiple Charts

Priya is building a complete student performance dashboard. Here is how to lay out four charts on one page:

```html
<h1>TechPath Institute — Student Dashboard</h1>
<p>Batch: 2026 | Student: Rahul Sharma | City: Bhopal</p>

<div class="dashboard-grid">
    <div class="chart-card">
        <h3>Module Marks</h3>
        <canvas id="marksChart"></canvas>
    </div>

    <div class="chart-card">
        <h3>Attendance Trend</h3>
        <canvas id="attendanceChart"></canvas>
    </div>

    <div class="chart-card">
        <h3>Course Completion</h3>
        <canvas id="completionChart"></canvas>
    </div>

    <div class="chart-card">
        <h3>Skill Radar</h3>
        <canvas id="skillChart"></canvas>
    </div>
</div>

<style>
.dashboard-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
    gap: 20px;
    padding: 20px;
}

.chart-card {
    background: white;
    border-radius: 8px;
    padding: 20px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.chart-card h3 {
    margin-top: 0;
    color: #333;
    border-bottom: 2px solid #2196F3;
    padding-bottom: 8px;
}
</style>
```

This uses CSS Grid with `auto-fit` and `minmax` — four charts in two columns on desktop, stacking to one column on mobile. No media queries needed.

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Chart canvas has no width/height | Wrap in a container `div` with defined width |
| Chart is blurry on Retina screens | Chart.js handles this automatically — do not set canvas width/height in HTML |
| Data does not update | Call `chart.update()` after changing `chart.data` |
| Forgot to destroy old chart | Call `chart.destroy()` before creating a new one on the same canvas |
| Colors are hard to read | Use high-contrast colors, test for color blindness |

---

## Key Takeaways

1. Charts turn raw numbers into visual stories — always prefer a chart over a table for presentations
2. Chart.js is simple and lightweight — perfect for dashboards and reports
3. Plotly.js is heavier but gives zoom, pan, and export — use it for data exploration
4. Load chart data from your Python API using `fetch()` — never hardcode data in production
5. Always make charts responsive by setting `responsive: true` and wrapping `<canvas>` in a container
6. Use CSS Grid for multi-chart dashboard layouts — it handles responsiveness automatically

---

*TechPath Institute — Python Full Stack Development Program*
