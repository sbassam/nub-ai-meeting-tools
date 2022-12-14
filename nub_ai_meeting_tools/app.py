import time
from pyvis.network import json
import streamlit as st
import streamlit.components.v1 as components
from streamlit.elements import progress
from core import Graph
import nltk
from nltk.tokenize import sent_tokenize
import io
from utils import get_generated_text, extract_graph_elements
import copy
import nltk
st.set_page_config(page_title='Meeting Graph', layout='centered')
st.image('nub_ai_meeting_tools/full-stack-logo.png')
nltk.download('punkt')
st.title("Meeting Knowledge Graph Generator")

input_file = st.file_uploader(label="Upload meeting transcript txt file")

initial_graph, data_display, user_corrected_graph = st.tabs(['Meeting Knowledge Graph', 'Graph Data', 'User-corrected Graph'])

@st.cache
def get_all_graph_elements(sent_list):
    graph_element_list = []
    # progress = 0
    # st.progress(progress)
    for sent in sent_list:
        # progress += 100/len(sent_list)
        # st.progress(progress)
        generated_text = get_generated_text(sent)
        graph_elements = extract_graph_elements(generated_text)
        graph_element_list.append(graph_elements)
    # st.progress(100)
    # st.balloons()
    return graph_element_list


if input_file:
    # read and parse transcript into sentences
    stringio = io.StringIO(input_file.getvalue().decode("utf-8"))
    string_data = stringio.read()
    sent_list = sent_tokenize(string_data)
    graph_element_list = get_all_graph_elements(sent_list)
    graph_element_list_fixed = copy.deepcopy(graph_element_list)

    

    for i, sent in enumerate(sent_list):
        with data_display:
            st.text(f'Sentence {i}: {sent}')
            col1, col2 = st.columns(2)
            with col1:
                st.text(f'Derived Nodes: \n')
                st.text(f'  Name: {graph_element_list[i]["src"][0]}')
                st.text(f'  Task: {graph_element_list[i]["dest"][0]}')
                st.text(f'  Timeline: {graph_element_list[i]["edge"][2]}')
            with col2:
                st.write(f'See something wrong?')
                fixed_name = st.text_input('Enter the correct Name', key=sent+'fixname')
                if fixed_name:
                    graph_element_list_fixed[i]["src"] = (fixed_name, fixed_name, 'person')
                fixed_task = st.text_input('Enter the correct Task', key=sent+'fixtask')
                if fixed_task:
                    graph_element_list_fixed[i]["dest"] = (fixed_task, fixed_task, 'task')
                fixed_timeline = st.text_input('Enter the correct Timeline', key=sent+'fixtimeline')
                if fixed_timeline:
                    name, task, timeline, title = graph_element_list[i]["edge"]
                    graph_element_list_fixed[i]["edge"] = (fixed_timeline, task, timeline, title)
                graph_element_list_fixed[i]["edge"] = (
                    graph_element_list_fixed[i]["src"][0],
                    graph_element_list_fixed[i]["dest"][0],
                    graph_element_list_fixed[i]["edge"][2],
                    graph_element_list_fixed[i]["edge"][3])
            st.text('-'*100)


           
    with initial_graph:
        knowledge_graph = Graph('meeting_knowledge_graph.html')
        for graph_elements in graph_element_list:
            # st.write(f'this is the element {graph_elements}')
            knowledge_graph.add_node(*graph_elements["src"])
            knowledge_graph.add_node(*graph_elements["dest"])
            knowledge_graph.add_edge(*graph_elements["edge"])
        knowledge_graph.display_graph()
        source_code = knowledge_graph.get_html()
        components.html(source_code, height=800, width=800)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(label='Number of sentences', value=len(sent_list))
        with col2:
            st.metric(label='Number of nodes', value=knowledge_graph.get_node_count())
        with col3:
            st.metric(label='Number of edges', value=knowledge_graph.get_edge_count())

    
    with user_corrected_graph:
        user_data_submission = st.button('Submit Correction')
        if user_data_submission:
            bar = st.progress(10)
            # commented out for now to prevent sensitive data from being saved
            # with open('user_corrected_data.txt', 'w') as file:
            #     file.write(json.dumps(graph_element_list_fixed))
            time.sleep(.5)
            bar.progress(100)
            st.text('Submitted! Thanks for the contribution!')
            time.sleep(1)
            bar.progress(0)
            
        
        corrected_knowledge_graph = Graph('corrected_graph.html')

        for graph_elements in graph_element_list_fixed:
            corrected_knowledge_graph.add_node(*graph_elements["src"])
            corrected_knowledge_graph.add_node(*graph_elements["dest"])
            corrected_knowledge_graph.add_edge(*graph_elements["edge"])
        corrected_knowledge_graph.display_graph()
        corrected_source_code = corrected_knowledge_graph.get_html()
        components.html(corrected_source_code, height=800, width=800)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(label='Number of sentences', value=len(sent_list))
        with col2:
            st.metric(label='Number of nodes', value=corrected_knowledge_graph.get_node_count())
        with col3:
            st.metric(label='Number of edges', value=corrected_knowledge_graph.get_edge_count())

