from transformers import pipeline
import torch

# Use the summarization pipeline
summarizer = pipeline("summarization")

token = "xoxb-1422030608644-7284571152564-RTT4pxfF4LJmbcyExbWdXUvh"

app_level_tokn = "xapp-1-A078NN8A6RX-7294762556993-84197c4a80043ed5b9b370a411d4b213b8f51fdf3d941ebd86313a949621b618"

if torch.cuda.is_available():
    summarizer = summarizer.to('cuda')
    print('Using Cuda\n')
else:
    print('Not Using Cuda\n')


def summarize_messages_in_chunks(messages, chunk_size=500):
    # Break the text into manageable chunks
    chunks = []
    current_chunk = []
    current_length = 0
    
    for msg in messages:
        msg_length = len(msg['text'])
        if current_length + msg_length > chunk_size:
            chunks.append("\n".join(current_chunk))
            current_chunk = []
            current_length = 0
        current_chunk.append(msg['text'])
        current_length += msg_length
    
    # Don't forget to add the last chunk
    if current_chunk:
        chunks.append("\n".join(current_chunk))
    
    # Summarize each chunk separately and concatenate the results
    summaries = [summarizer(chunk, max_length=250, min_length=40, do_sample=False)[0]['summary_text'] for chunk in chunks]
    
    # Combine all chunk summaries into one
    final_summary = " ".join(summaries)
    
    return final_summary

# Example usage
messages = [
    {"text": "Hello Shy,  On Monday we have the next Israel monthly catch up.   The agenda covers performance management, a sales update and a review of the integration video.   I thought it might be useful to also cover a little on the company day - what it is, what to expect, why we're having it.   I thought you & Nelson might be able to cover this?  We only have 30 mins for the whole meeting, so this would be maybe 5 minutes, to give some highlights, get people excited about it. Are you happy to do this?  Sorry for the late notice, I realise you are not in today, and Nelson won't be in tomorrow, but I am hoping that it won't take much prep.   thanks Shy (edited) "},
    {"text": "So we can get content prepared for next weeks Product Demo & Learning and future sessions following the discussion on Monday, please can you add agenda items like knowledge sharing in the :thread: and add any people you need help with either puling the content together or presenting. I think it’ll be worthwhile using D&L sessions as much as possible rather than Munch & Learn, we can look to extending some session if needed depending on the agenda. Thanks."},
    {"text": "Hi @igor.pechersky @ben.marnan Integrated Content2Persona approach described in the Coda doc In the v1, used 500 top apps by coverage Ignore group scores, keep all groups that appear in app to persona response Adding new features that are persona counters RoC score is 0.76 that is pretty the same as for the old version (0.78) More in slides"},
    # Add more messages as needed
]

# Example usage
summary = summarize_messages_in_chunks(messages)
print(summary)

