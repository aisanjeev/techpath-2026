# Module 06 — Fundamentals of AI — Quick Revision Notes

---

## Key Definitions
- **AI** = Machines that mimic human intelligence (learning, reasoning, problem-solving)
- **ML (Machine Learning)** = AI that learns from data without explicit programming
- **DL (Deep Learning)** = ML using neural networks with many layers
- **GenAI (Generative AI)** = AI that creates new content (text, images, code, music)
- **LLM (Large Language Model)** = GenAI trained on massive text data (ChatGPT, Claude)

## Relationship: AI > ML > DL > GenAI > LLM
```
AI (broad field)
└── Machine Learning (learns from data)
    └── Deep Learning (neural networks)
        └── Generative AI (creates content)
            └── LLMs (language-specific GenAI)
```

## Types of Machine Learning
| Type | How It Learns | Example |
|------|-------------|---------|
| **Supervised** | Labeled data (input→output pairs) | Spam filter (email→spam/not spam) |
| **Unsupervised** | Unlabeled data (finds patterns) | Customer segmentation |
| **Reinforcement** | Trial and error (rewards/penalties) | Game-playing AI, self-driving cars |

## AI in Daily Life
| Service | AI Used | How |
|---------|---------|-----|
| YouTube/Netflix | Recommendation system | Suggests videos based on watch history |
| Google Search | NLP + ranking | Understands queries, ranks results |
| Gmail | Spam filter + Smart Reply | Blocks spam, suggests short replies |
| Google Maps | Route optimization | Predicts traffic, finds fastest route |
| Alexa/Siri | Speech recognition + NLP | Converts voice to text, understands intent |
| Instagram | Image recognition | Auto-tags people, content moderation |
| UPI/Banking | Fraud detection | Flags unusual transactions |

## How LLMs Work (Simplified)
1. **Training**: Read billions of text documents from the internet
2. **Tokenization**: Break text into tokens (word pieces)
3. **Pattern Learning**: Learn statistical patterns (which words follow which)
4. **Prediction**: Generate text by predicting the most likely next token
5. **Fine-tuning**: Adjust behavior for specific tasks (chat, code, translation)

## Key AI Concepts
| Concept | Meaning |
|---------|---------|
| **Training data** | The data AI learns from |
| **Model** | The trained AI system |
| **Inference** | Using the model to make predictions |
| **Hallucination** | AI confidently stating wrong information |
| **Token** | A piece of text (roughly ¾ of a word) |
| **Prompt** | Your instruction/question to the AI |
| **Context window** | How much text the AI can process at once |
| **Temperature** | Controls randomness (0=focused, 1=creative) |
| **Fine-tuning** | Training a model further on specific data |
| **Bias** | AI reflecting prejudices from its training data |

## AI Ethics
- **Bias**: AI can discriminate if training data is biased
- **Privacy**: AI trained on personal data raises privacy concerns
- **Job displacement**: Some jobs will change or disappear
- **Deepfakes**: AI-generated fake videos/audio
- **Accountability**: Who's responsible when AI makes mistakes?
- **Transparency**: Should AI explain its decisions? (Explainable AI)

## Prompt Engineering Basics
- **Be specific**: "Write a 3-paragraph email" not "Write an email"
- **Give context**: "You are a Python teacher explaining to beginners"
- **Show examples**: "Format like this: Name — Role — City"
- **Set constraints**: "Under 100 words, use simple English"
- **Iterate**: If first result isn't right, refine your prompt
