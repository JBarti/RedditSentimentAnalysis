# Reddit Sentiment Analysis Dashboard

A powerful web application that analyzes the sentiment of Reddit posts and their comments using state-of-the-art natural language processing. Built with Streamlit and powered by Hugging Face transformers, this tool provides comprehensive emotional analysis and interactive visualizations.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.50.0-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 🌟 Features

- **Real-time Sentiment Analysis**: Analyze any Reddit post and its comments instantly
- **7 Emotion Categories**: Detects joy, neutral, anger, disgust, sadness, fear, and surprise
- **Interactive Visualizations**:
  - Pie charts showing sentiment distribution
  - Score distribution by sentiment
  - Scatter plots correlating comment length with score
  - Word clouds for each sentiment category
- **Comment Depth Filtering**: Filter comments by their depth in the conversation thread
- **Emoji Processing**: Intelligent emoji recognition and conversion to meaningful text
- **Pre-loaded Example**: Explore the tool with a sample analysis

## 📋 Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [How It Works](#how-it-works)
- [Contributing](#contributing)
- [License](#license)
- [Author](#author)

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Reddit API credentials (already configured in the code)

### Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/JBarti/RedditSentimentAnalysis.git
   cd RedditSentimentAnalysis
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## 💻 Usage

### Running the Dashboard

Start the Streamlit application:

```bash
streamlit run dashboard.py
```

The dashboard will open automatically in your default web browser at `http://localhost:8501`.

### Analyzing a Reddit Post

1. Enter a Reddit post URL in the input field (e.g., `https://www.reddit.com/r/python/comments/...`)
2. Click the **Run** button
3. Wait for the analysis to complete (this may take a few moments depending on the number of comments)
4. Explore the interactive visualizations and insights

### Using the Command Line Sentiment Analyzer

For direct sentiment classification:

```bash
cd app
python sentiment.py
```

Then enter text when prompted. Type 'q' to quit.

## 🛠️ Technology Stack

### Core Technologies

- **[Streamlit](https://streamlit.io/)** - Web application framework
- **[Hugging Face Transformers](https://huggingface.co/transformers/)** - NLP and sentiment analysis
- **[PRAW](https://praw.readthedocs.io/)** - Reddit API wrapper

### Sentiment Model

- **Model**: `j-hartmann/emotion-english-distilroberta-base`
- **Architecture**: DistilRoBERTa
- **Categories**: 7 emotions (joy, neutral, anger, disgust, sadness, fear, surprise)

### Visualization Libraries

- **[Plotly Express](https://plotly.com/python/plotly-express/)** - Interactive charts
- **[WordCloud](https://github.com/amueller/word_cloud)** - Word cloud generation
- **[Matplotlib](https://matplotlib.org/)** - Additional plotting capabilities

### Data Processing

- **[Pandas](https://pandas.pydata.org/)** - Data manipulation and analysis
- **[NumPy](https://numpy.org/)** - Numerical computations

## 📁 Project Structure

```
RedditSentimentAnalysis/
│
├── app/
│   ├── dashboard_helpers/
│   │   ├── avatar.py                 # User avatar component
│   │   ├── load_example_analysis.py  # Load example data
│   │   ├── mappings.py               # Sentiment color/emoji mappings
│   │   └── run_sentiment_analysis.py # Main analysis logic
│   │
│   ├── emoji_cleaner.py              # Emoji to text conversion
│   ├── reddit_client.py              # Reddit API client
│   └── sentiment.py                  # Sentiment classification engine
│
├── misc/
│   └── emojis.csv                    # Emoji name mappings
│
├── dashboard.py                      # Main Streamlit application
├── example_sentiment_analysis.json   # Pre-loaded example data
├── requirements.txt                  # Python dependencies
├── .gitignore                        # Git ignore rules
└── README.md                         # This file
```

## ⚙️ Configuration

### Reddit API Credentials

The Reddit client is configured with read-only access. Credentials are embedded in `app/reddit_client.py`:

```python
client = Reddit(
    client_id="k8a8tz48Q_B3eK8WDfMkng",
    client_secret="ZNzO37w4GbIx_S0rBzE2JUOTR9opIw",
    user_agent="Comment Extraction (by u/JaSamBatak)",
)
```

**Note**: These are read-only credentials. For production use, consider using environment variables.

### Sentiment Model Configuration

The sentiment classifier uses the `j-hartmann/emotion-english-distilroberta-base` model. On first run, it will be downloaded automatically from Hugging Face (approximately 300MB).

### Streamlit Secrets

For sensitive configurations, create `.streamlit/secrets.toml` (already in `.gitignore`):

```toml
[reddit]
client_id = "your_client_id"
client_secret = "your_client_secret"
user_agent = "your_user_agent"
```

## 🔍 How It Works

### Sentiment Analysis Pipeline

1. **Data Extraction**: Uses PRAW to fetch Reddit post and comments
2. **Text Preprocessing**: Cleans emojis and truncates to model's max length (512 tokens)
3. **Sentiment Classification**: Processes text through DistilRoBERTa model
4. **Aggregation**: Combines individual sentiment scores into analytics
5. **Visualization**: Renders interactive charts and word clouds

### Emoji Processing

The application converts emojis to their textual representations to improve sentiment analysis accuracy:

```python
# Example: "I love this! 😍" → "I love this! <smiling face with heart-shaped eyes>"
```

### Comment Depth

Comments are organized by depth (0 = top-level, 1 = reply to top-level, etc.) allowing for thread-specific analysis.

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit your changes**: `git commit -m 'Add amazing feature'`
4. **Push to the branch**: `git push origin feature/amazing-feature`
5. **Open a Pull Request**

### Development Guidelines

- Follow PEP 8 style guidelines
- Add comments for complex logic
- Test your changes with various Reddit posts
- Update documentation as needed

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👤 Author

**Josip Bartulović**

- LinkedIn: [Josip Bartulović](https://www.linkedin.com/in/josip-bartulovic/)
- Email: josip.bartulovic3@gmail.com
- Reddit: u/JaSamBatak

### About the Developer

Data Specialist | Automation Enthusiast | Tech Nerd

I help businesses streamline their data processes, automate repetitive tasks, and build data products that drive growth.

## 🙏 Acknowledgments

- [Hugging Face](https://huggingface.co/) for the emotion classification model
- [Streamlit](https://streamlit.io/) for the amazing web framework
- [PRAW](https://praw.readthedocs.io/) for Reddit API access
- The open-source community for various libraries used in this project

## 📊 Example Use Cases

- **Community Management**: Understand sentiment trends in your subreddit
- **Market Research**: Analyze public opinion about products or topics
- **Content Strategy**: Identify what types of posts generate positive engagement
- **Academic Research**: Study emotional patterns in online discussions
- **Brand Monitoring**: Track sentiment around your brand on Reddit

## 🚧 Future Enhancements

- [ ] User authentication for personal Reddit access
- [ ] Export analysis results to CSV/JSON
- [ ] Historical sentiment tracking over time
- [ ] Multi-post comparison
- [ ] Customizable sentiment models
- [ ] API endpoint for programmatic access
- [ ] Subreddit-level analysis

---

Made with ❤️ by [Josip Bartulović](https://www.linkedin.com/in/josip-bartulovic/)
