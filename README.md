# Graph-Rendering

This fork adds a few new features to the graph visualizer by Russell Schwartz. These features are listed below.

1. You may now input a list of dependencies between nodes in an ordinary text file, and Python will automatically parse it into a neat graph for you. An example of the dependency syntax, as well as the output, is in the `sample_data` folder. The motivation for this is in creating a visualizer for different classes and their (sometimes complicated) prerequisite structure.

2. This also adds an attractive force feature to keep disconnected parts of a graph from repelling away from the rest, instead making large tails appear to curl back toward the center. This makes it much easier to see all nodes in the graph (with labels) at once, rather than needing to pan around or zoom.

3. Springs can now have (easily customizable) arrowheads to indicate a directional relationship between two bodies in the graph.

See one of the sample images below:

![Sample Image](https://github.com/StardustGogeta/Graph-Rendering/blob/master/sample_data/SampleOutput5.PNG)
