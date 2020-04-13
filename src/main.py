import pathlib
import Render, DependencyParser

if __name__ == '__main__':
    graph_text = ""
    path = pathlib.Path(__file__).parent.parent / "sample_data/dependencyList.txt"
    with open(path) as dependencyList:
        graph_text = dependencyList.read()

    system = DependencyParser.parse(graph_text, friction=.65, repulsion=0.15, attraction=0.08)
    # print(system.__dict__)
    Render.run_system(system)
    