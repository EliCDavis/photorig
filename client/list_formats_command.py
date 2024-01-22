from pygrabber.dshow_graph import FilterGraph
import logging

def list_formats_command(args):
    graph = FilterGraph()
    graph.add_video_input_device(args.camera_index)
    formats = graph.get_input_device().get_formats()
    logging.info(f"Available formats for {graph.get_input_device().Name}")
    for f in formats:
        logging.info(f)