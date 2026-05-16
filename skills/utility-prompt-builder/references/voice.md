# Voice Reference — Voice Synthesis AI

## § ELEVENLABS

- Specify emotion, pacing, emphasis markers, and speech rate directly
- Use SSML-like markers for emphasis: indicate which words to stress, where to pause
- Prose descriptions of mood do not translate — specify parameters directly
- Voice cloning: describe the target voice's age, accent, pace, tone, and emotion register

**Prompt elements to specify:**
- Emotion: neutral, excited, sad, authoritative, whispering, shouting
- Pace: slow, normal, fast, with long pause before [word]
- Emphasis: stress the word "[word]" strongly
- Accent/language: specify if not English

**Example format:**
```
[Text to speak]
Voice direction: [Calm, measured pace. Slight pause after "however". Emphasize "never" with firm stress. American English, professional tone.]
```
