import nlpcloud


def get_generated_text(text):
    """
    Calls the NLP Cloud API and gets back the extracted entities Names, Tasks, and Timelines
    """

    client = nlpcloud.Client(
        "gpt-j", "a3df5c847f0db613892cb168dcbcc6dda79ed3a8", gpu=True)
    generation = client.generation(f"""[Text]: [John]: I have to create a new story for this. I'll finish this story by the end of the sprint.
        [Name]: John
        [Task]: create a new story, finish story
        [Timeline]: by the end of the sprint
        ###
        [Text]: [Cindy]: How is it going everyone? Anything fun this weekend?
        [Name]:  Cindy
        [Task]: 
        [Timeline]: 
        ###
        [Text]: [Prashant]: Grace, do you think we're good to go on the presentation? [Grace]: Yes, I should be able to socialize the presentation draft by the end of today.
        [Name]:  Grace
        [Task]: socialize the presentation draft
        [Timeline]: end of today
        ###
        [Text]: {text}
        """,
                                   top_p=0,
                                   length_no_input=True,
                                   end_sequence="###",
                                   remove_end_sequence=True,
                                   remove_input=True)
    # print(generation["generated_text"])
    return generation["generated_text"]


def extract_graph_elements(generated_text):
    """
    Extracts nodes and edges from generated text the output of get_generated_text()
    """
    name, task, timeline = generated_text.strip().rstrip('###').strip().splitlines()
    name = name.split(':')[1].strip()
    task = task.split(':')[1].strip()
    timeline = timeline.split(':')[1].strip()
    return {"src": (name, name, 'person'), "dest": (task, task, 'task'), "edge": (name, task, timeline, 'is assigned')}


if __name__ == '__main__':
    print(get_generated_text(
        "[Anna]: We have to set up a meeting to go over the details of the demo project today."))
