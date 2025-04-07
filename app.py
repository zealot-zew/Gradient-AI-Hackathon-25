import streamlit as st
import random
from collections import Counter
import re
import os
import time
from gtts import gTTS
import base64
from io import BytesIO
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_mood_topic_selector():
    """Step 1: Creates a UI for mood and topic selection"""
    st.title("🌈 Learning Adventure")
    st.subheader("Hey there! Let's learn something awesome today!")
    st.markdown("""
    <style>
    /* Target all radio button labels */
    .stRadio > div > label {
        color: black !important;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("### How are you feeling today? 😊")
    mood = st.radio(
    "Pick your mood:",
    ["Energetic 🏃", "Curious 🔍", "Bored 😴", "Playful 🎮", 
     "Calm 🌊", "Frustrated 😣", "Focused 🎯"],
    index=1  # Default to "Curious"
    )
    
    # Clean the mood string to remove emoji
    mood = mood.split()[0]
    
    # Topic selection with examples for inspiration
    st.markdown("### What would you like to learn about today?")
    topic_examples = "Examples: Space, Dinosaurs, Numbers, Plants, Animals, Music, Art"
    topic = st.text_input("Enter your topic:", placeholder=topic_examples)
    
    # Submit button with some visual appeal
    if st.button("Let's Go! 🚀", use_container_width=True):
        if topic:
            return {"mood": mood, "topic": topic}
        else:
            st.error("Please enter a topic you'd like to learn about!")
            return None
    return None

def simulate_cookie_data():
    """Step 2: Simulate browser cookie data for content preferences"""
    st.markdown("### 🍪 Analyzing your favorite video styles...")
    
    # All possible content formats
    content_formats = [
        "Animated Story",
        "Musical / Songs",
        "Gamified Lessons",
        "Roleplay or Skits",
        "Cartoon Explainers",
        "Doodle/Whiteboard Style",
        "ASMR/Narration"
    ]
    
    # Create a weighted random distribution of viewed content
    # This simulates a child's viewing history from cookies
    num_views = 100  # Total number of simulated video views
    
    # For realism, we'll make the distribution slightly skewed
    # Some formats will be viewed more often than others
    weights = [random.uniform(0.5, 2.0) for _ in range(len(content_formats))]
    
    # Normalize weights to sum to 1
    total_weight = sum(weights)
    weights = [w/total_weight for w in weights]
    
    # Generate the simulated viewing history
    viewing_history = random.choices(content_formats, weights=weights, k=num_views)
    
    # Count occurrences of each format
    format_counter = Counter(viewing_history)
    
    # Get the top 3 most viewed formats
    top_formats = format_counter.most_common(3)
    
    # Display the simulated cookie data with a simple visualization
    st.write("Based on your previous viewing habits:")
    
    # Create a fun visualization of the data
    for format_name, count in format_counter.most_common():
        percentage = (count / num_views) * 100
        st.write(f"{format_name}: {percentage:.1f}%")
        st.progress(percentage / 100)
    
    st.markdown("### 🎯 Your top 3 favorite formats:")
    for i, (format_name, count) in enumerate(top_formats, 1):
        st.markdown(f"**{i}. {format_name}** ({count} views)")
    
    # Return just the names of the top 3 formats
    return [format_name for format_name, _ in top_formats]

def generate_ai_prompt(mood, topic, top_formats):
    """Step 3: Generate a prompt for an LLM based on mood, topic, and formats"""
    st.markdown("### 🧠 Creating your personalized lesson...")
    
    # Create a dictionary of mood-based learning approaches
    mood_approaches = {
        "Energetic": "active learning with movement breaks, high energy delivery, quick pace changes",
        "Curious": "inquiry-based exploration with surprising facts and 'did you know' moments",
        "Bored": "highly engaging content with humor, surprising facts, and interactive elements",
        "Playful": "game-like elements, playful metaphors, and creative challenges",
        "Calm": "gentle pacing, soothing tone, organized structure with clear transitions",
        "Frustrated": "simple explanations, frequent encouragement, broken into very small achievable steps",
        "Focused": "deeper dives into the topic, slightly more advanced content, analytical thinking"
    }
    
    # Create a dictionary of format-based instructions
    format_instructions = {
        "Animated Story": "animated story with characters who discover concepts through adventures",
        "Musical / Songs": "catchy educational songs and rhythmic patterns to help memorization",
        "Gamified Lessons": "game-like scenarios with challenges, rewards, and achievements",
        "Roleplay or Skits": "dialogue-based script with characters taking on different roles",
        "Cartoon Explainers": "visually rich explanations with cartoon characters and visual metaphors",
        "Doodle/Whiteboard Style": "step-by-step visual explanations like on a whiteboard with doodles",
        "ASMR/Narration": "calm, clear narration with descriptive language and guided imagination"
    }
    
    # Special needs adaptations
    adaptations = """
    - Use clear, concise language with simple sentence structures
    - Break information into small, digestible chunks
    - Incorporate frequent repetition of key concepts
    - Use visual cues and memory aids throughout
    - Include movement breaks or interactive moments every 2-3 minutes
    - Provide multiple ways to understand each concept (visual, auditory, kinesthetic)
    """
    
    # Get the specific approach based on mood and formats
    mood_strategy = mood_approaches.get(mood, mood_approaches["Curious"])
    format_strategies = [format_instructions.get(format_name, "") for format_name in top_formats]
    
    # Generate the prompt for the LLM
    prompt = f"""
    Create an engaging educational script on "{topic}" for a {mood.lower()} child aged 6-12 with cognitive differences like ADHD and dyslexia.
    
    The lesson should be delivered in one of these formats (in order of preference):
    1. {top_formats[0]}
    2. {top_formats[1]}
    3. {top_formats[2]}
    
    Specifically, make it:
    - Suitable for the child's {mood.lower()} mood: {mood_strategy}
    - Primarily in the style of {top_formats[0]}: {format_instructions.get(top_formats[0], "")}
    - With elements from {top_formats[1]} and {top_formats[2]} where appropriate
    
    Cognitive support adaptations:
    {adaptations}
    
    Keep the script between 3-5 minutes when performed, with clear markers for visual elements.
    Include a title, introduction, body, and conclusion with a quick knowledge check.
    """
    
    # Display the generated prompt with a "thinking" spinner
    with st.spinner("Generating your personalized lesson... ✨"):
        st.write("Creating a lesson that matches your needs...")
        
        # Show a preview of how the system is personalizing content
        st.info(f"Personalizing for a {mood.lower()} learner who wants to learn about {topic}!")
        st.write(f"Primary format: **{top_formats[0]}**")
        
        # For demonstration, we'll delay briefly to simulate API call time
        time.sleep(2)
    
    return prompt

def get_ai_response(prompt):
    """Get response from an LLM API using the generated prompt"""
    st.write("Asking our AI teacher to create your lesson...")
    
    try:
        # Optional: If you have an OpenAI API key configured
        if os.getenv("OPENAI_API_KEY"):
            import openai
            openai.api_key = os.getenv("OPENAI_API_KEY")
            
            response = openai.ChatCompletion.create(
                model="gpt-4",  # or another appropriate model
                messages=[
                    {"role": "system", "content": "You are an educational content creator specializing in creating engaging content for children with cognitive differences."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1500,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        # Mock response for demonstration
        else:
            st.warning("No API key found. Using mock response for demonstration.")
            time.sleep(2)  # Simulate API delay
            
            # This is a sample response - in production, you'd get this from the API
            topic = prompt.split("script on \"")[1].split("\"")[0]
            
            if "dinosaur" in topic.lower():
                return f"""
                # Dino Discovery Adventure!

                [OPENING SONG]
                🎵 Dinosaurs, dinosaurs, long, long ago,
                Some were fast, some were slow!
                Dinosaurs, dinosaurs, big and small,
                Let's learn about them all! 🎵

                [ANIMATED INTRO: Cartoon dinosaurs marching across the screen]

                NARRATOR: Welcome to Dino Discovery Adventure! Today we're going back in time to meet some AMAZING creatures called DINOSAURS!

                [GAME ELEMENT: When children say "dinosaurs," animated footprints appear]

                Dinosaurs lived on Earth a VERY long time ago - more than 65 MILLION years ago! That's WAY before people existed!

                [ANIMATED SEQUENCE: Timeline showing dinosaurs then humans]

                There were many different kinds of dinosaurs:
                1. Some were HUGE like Brachiosaurus! (Stand up tall with arms stretched high)
                2. Some were TINY like Compsognathus! (Crouch down low)
                3. Some had SHARP TEETH like T-Rex! (Make chomping motions)
                4. Some ate PLANTS like Triceratops! (Pretend to munch leaves)

                [MOVEMENT BREAK: Children act out different dinosaur movements]

                [SONG BREAK]
                🎵 Stegosaurus had plates on its back,
                T-Rex had arms that were tiny,
                Pterodactyl could fly in the sky,
                Triceratops had three horns on its head! 🎵

                Scientists who study dinosaurs are called PALEONTOLOGISTS.
                Let's say that big word together: PAL-E-ON-TOL-O-GISTS!

                [GAME ELEMENT: Dinosaur dig where children find hidden fossils]

                Paleontologists find dinosaur bones called FOSSILS in the ground.
                These fossils help us learn what dinosaurs looked like and how they lived.

                [QUICK KNOWLEDGE CHECK]
                What do we call the scientists who study dinosaurs?
                (Pause for response)
                Great job! Paleontologists!

                What do we call dinosaur bones found in the ground?
                (Pause for response)
                That's right! Fossils!

                [CLOSING SONG]
                🎵 Now we know about dinosaurs,
                They lived long, long ago.
                Though they're gone from our world today,
                Their fossils help us know! 🎵

                THE END! You're now a dinosaur expert! ROAR!
                """
            else:
                return f"""
                # The Wonderful World of {topic}!

                [OPENING SONG]
                🎵 Learning, learning, it's so fun,
                Learning about {topic}!
                So many things to discover,
                Let's explore together! 🎵

                [ANIMATED INTRO: Cartoon characters looking excited with magnifying glasses]

                NARRATOR: Welcome to The Wonderful World of {topic}! Today we're going to learn amazing facts and have fun together!

                [GAME ELEMENT: When children repeat "{topic}" correctly, animated stars appear]

                {topic} is an amazing subject to learn about! Did you know that {topic} is all around us?

                [ANIMATED SEQUENCE: Showing examples of {topic} in everyday life]

                Here are some cool things about {topic}:
                1. {topic} has been around for a very long time!
                2. People use {topic} every day!
                3. {topic} helps us understand our world better!

                [MOVEMENT BREAK: Children stand up and act out aspects of {topic}]

                [SONG BREAK]
                🎵 {topic}, {topic}, so much to learn,
                Every day we discover more!
                {topic}, {topic}, now we know,
                Learning makes us grow! 🎵

                Let's dive deeper into {topic}! There are so many interesting parts to explore.

                [GAME ELEMENT: Interactive quiz where children identify parts of {topic}]

                [QUICK KNOWLEDGE CHECK]
                What's one interesting thing about {topic} that you learned today?
                (Pause for response)
                That's right! Great job remembering!

                [CLOSING SONG]
                🎵 Now we know about {topic},
                We've learned so many things!
                We can share with our friends and family,
                All the joy that knowledge brings! 🎵

                THE END! You're now a {topic} expert! Great job learning today!
                """
    
    except Exception as e:
        st.error(f"Error generating AI response: {str(e)}")
        return "I'm sorry, I couldn't generate a lesson right now. Let's try again later!"

def process_ai_response(response):
    """Process the AI response to add formatting and styling"""
    # Extract title if it exists
    title_match = re.search(r'^#\s+(.*?)$', response, re.MULTILINE)
    title = title_match.group(1) if title_match else "Your Personalized Lesson"
    
    # Remove the title from the response if it was found
    if title_match:
        response = response.replace(title_match.group(0), '')
    
    # Format title
    formatted_response = f'<div class="lesson-title">{title}</div>'
    
    # Replace markdown headers with styled HTML
    response = re.sub(r'^##\s+(.*?)$', r'<h3>\1</h3>', response, flags=re.MULTILINE)
    
    # Format special sections
    response = re.sub(r'\[SONG.*?\](.*?)\n\n', r'<div class="song">\1</div>', response, flags=re.DOTALL)
    response = re.sub(r'\[MOVEMENT.*?\](.*?)\n\n', r'<div class="movement">\1</div>', response, flags=re.DOTALL)
    response = re.sub(r'\[GAME.*?\](.*?)\n\n', r'<div class="movement">\1</div>', response, flags=re.DOTALL)
    response = re.sub(r'\[QUICK KNOWLEDGE CHECK\](.*?)\n\n', r'<div class="knowledge-check"><strong>Quick Check:</strong>\1</div>', response, flags=re.DOTALL)
    
    # Format other common patterns
    response = re.sub(r'\[.*?\]', r'<strong>\g<0></strong>', response)  # Make [TAGS] bold
    response = re.sub(r'\*\*(.*?)\*\*', r'<span class="highlight">\1</span>', response)  # Highlight **text**
    response = re.sub(r'\n\n', r'</div><div class="lesson-section">', response)  # Section breaks
    
    # Format emoji
    response = re.sub(r'([\U0001F300-\U0001F6FF])', r'<span style="font-size: 24px;">\1</span>', response)
    
    # Complete the formatting
    formatted_response += f'<div class="lesson-section">{response}</div>'
    
    return formatted_response

def display_related_resources(topic):
    """Display mock related educational resources based on the topic"""
    # Mock YouTube video recommendations
    mock_videos = [
        {
            "title": f"Fun {topic} Facts for Kids",
            "channel": "Kids Learning Tube",
            "length": "4:32",
            "views": "1.2M views",
            "thumbnail": "https://via.placeholder.com/120x90.png?text=Video+1"
        },
        {
            "title": f"{topic} Song | Educational Music Video",
            "channel": "Educational Songs",
            "length": "3:18",
            "views": "876K views",
            "thumbnail": "https://via.placeholder.com/120x90.png?text=Video+2"
        },
        {
            "title": f"{topic} Explained: Science for Kids",
            "channel": "Science Explorers",
            "length": "5:42",
            "views": "2.4M views",
            "thumbnail": "https://via.placeholder.com/120x90.png?text=Video+3"
        }
    ]
    
    # Display the mock videos in a grid
    st.write("Here are some related videos you might enjoy:")
    
    # Create columns for the videos
    cols = st.columns(3)
    
    for i, video in enumerate(mock_videos):
        with cols[i]:
            st.image(video["thumbnail"], use_column_width=True)
            st.write(f"**{video['title']}**")
            st.write(f"{video['channel']} • {video['views']}")
            st.write(f"Length: {video['length']}")
    
    # Add some educational websites as resources
    st.write("---")
    st.write("**Learning Activities:**")
    
    activity_cols = st.columns(2)
    
    with activity_cols[0]:
        st.write(f"🎮 **Interactive {topic} Game**")
        st.write("Practice what you've learned with fun activities!")
        if st.button("Open Game", key="game"):
            st.info(f"This would open an interactive {topic} game in a real application.")
    
    with activity_cols[1]:
        st.write(f"📝 **{topic} Worksheet**")
        st.write("Download a printable activity sheet.")
        if st.button("Download Worksheet", key="worksheet"):
            st.info(f"This would download a {topic} worksheet in a real application.")

def display_lesson(ai_response):
    """Display the AI-generated lesson with formatting and optional features"""
    st.markdown("## 📺 Your Personalized Learning Video")
    
    # Create a colorful container for the lesson
    lesson_container = st.container()
    with lesson_container:
        st.markdown("""
        <style>
        .lesson-container {
            background-color: #f8f9fa;
            padding: 20 px;
            border-radius: 10 px;
            border: 2 px solid #6c757d;
        }
        .lesson-title {
            color: #007bff;
            text-align: center;
            font-size: 24 px;
            margin-bottom: 10 px;
        }
        .lesson-section {
            margin-top: 15 px;
            margin-bottom: 15 px;
            color: #000000
        }
        .highlight {
            background-color: #ffffff;
            padding: 2 px 5 px;
            border-radius: 3 px;
        }
        .song {
            background-color: #e6f7ff;
            padding: 10 px;
            border-radius: 5 px;
            font-style: italic;
        }
        .movement {
            background-color: #d4edda;
            padding: 10 px;
            border-radius: 5 px;
        }
        .knowledge-check {
            background-color: #f8d7da;
            padding: 10 px;
            border-radius: 5 px;
        }
        </style>
        """
        , unsafe_allow_html=True)
        
        # Process the AI response to add formatting
        formatted_response = process_ai_response(ai_response)
        
        # Display the formatted lesson
        st.markdown(f'<div class="lesson-container">{formatted_response}</div>', unsafe_allow_html=True)
    
    # Text-to-Speech feature
    st.markdown("## 🔊 Listen to your lesson")
    
    # Extract plain text without markdown or HTML for TTS
    plain_text = re.sub(r'<.*?>', '', ai_response)
    plain_text = re.sub(r'\[.*?\]', '', plain_text)
    plain_text = re.sub(r'\*\*(.*?)\*\*', r'\1', plain_text)
    
    # Create TTS options
    tts_option = st.radio(
        "Choose your text-to-speech option:",
        ["None", "Listen to Lesson", "Download Audio"]
    )
    
    if tts_option == "Listen to Lesson":
        # Use gTTS for online TTS
        try:
            with st.spinner("Preparing audio..."):
                tts = gTTS(text=plain_text, lang='en', slow=False)
                
                # Save to BytesIO object
                fp = BytesIO()
                tts.write_to_fp(fp)
                fp.seek(0)
                
                # Create a base64 encoded string
                audio_bytes = fp.read()
                audio_b64 = base64.b64encode(audio_bytes).decode()
                
                # Display audio player
                st.markdown(f"""
                <audio controls autoplay>
                  <source src="data:audio/mp3;base64,{audio_b64}" type="audio/mp3">
                  Your browser does not support the audio element.
                </audio>
                """, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error generating audio: {str(e)}")
            st.info("Please try the offline option if you're having issues.")
    
    elif tts_option == "Download Audio":
        try:
            with st.spinner("Preparing audio for download..."):
                tts = gTTS(text=plain_text, lang='en', slow=False)
                
                # Save to BytesIO object
                fp = BytesIO()
                tts.write_to_fp(fp)
                fp.seek(0)
                
                # Provide download button
                st.download_button(
                    label="Download Audio Lesson",
                    data=fp,
                    file_name="personalized_lesson.mp3",
                    mime="audio/mp3"
                )
        except Exception as e:
            st.error(f"Error generating downloadable audio: {str(e)}")
    
    # Find related videos (mock function)
    st.markdown("## 📚 Related Learning Resources")
    display_related_resources(st.session_state.user_selection['topic'])

def main():
    """Main application function"""
    st.set_page_config(
        page_title="Learning Adventure",
        page_icon="🧠",
        layout="centered"
    )
    
    # Apply custom CSS
    st.markdown("""
    <style>
    .stRadio > div {
        padding: 10px;
        background-color: #f0f8ff;
        border-radius: 10px;
    }
    .stButton button {
        background-color: #FFD700;
        color: #000000;
        font-size: 18px;
        font-weight: bold;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Initialize session state for workflow
    if 'step' not in st.session_state:
        st.session_state.step = 1
    
    # Step 1: Mood and Topic Selection
    if st.session_state.step == 1:
        user_selection = create_mood_topic_selector()
        if user_selection:
            st.session_state.user_selection = user_selection
            st.session_state.step = 2
            st.rerun()
    
    # Step 2: Cookie Simulation
    elif st.session_state.step == 2:
        st.write(f"You're feeling **{st.session_state.user_selection['mood']}** and want to learn about **{st.session_state.user_selection['topic']}**!")
        st.session_state.top_formats = simulate_cookie_data()
        
        if st.button("Continue to lesson creation! 📚", use_container_width=True):
            st.session_state.step = 3
            st.rerun()
    
    # Step 3: AI Prompt Generation
    elif st.session_state.step == 3:
        mood = st.session_state.user_selection['mood']
        topic = st.session_state.user_selection['topic']
        top_formats = st.session_state.top_formats
        
        # Generate the prompt
        prompt = generate_ai_prompt(mood, topic, top_formats)
        st.session_state.prompt = prompt
        
        # Create a collapsible section to show the actual prompt
        with st.expander("See the prompt we're using"):
            st.code(prompt)
        
        # Get AI response based on the prompt
        if st.button("Generate my lesson! 🚀", use_container_width=True):
            st.session_state.ai_response = get_ai_response(prompt)
            st.session_state.step = 4
            st.rerun()
    
    # Step 4: Display Final Lesson
    elif st.session_state.step == 4:
        # Display a header with the topic and mood
        st.header(f"Learning about {st.session_state.user_selection['topic']} 🎓")
        st.write(f"A lesson created for a {st.session_state.user_selection['mood'].lower()} learner")
        
        # Display the lesson with all formatting and features
        display_lesson(st.session_state.ai_response)
        
        # Restart button
        if st.button("Create another lesson! 🔄", use_container_width=True):
            # Reset the session state
            for key in list(st.session_state.keys()):
                if key != "step":
                    del st.session_state[key]
            st.session_state.step = 1
            st.rerun()

if __name__ == "__main__":
    main()