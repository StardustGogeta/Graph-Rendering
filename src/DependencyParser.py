import math
import Physics

def find_body_by_name(bodies, name):
    return [body for body in bodies if body.label == name][0]

# Generates bodies and springs as necessary

# Maintain a set of all unique bodies
# Make a spring for every link in the text file
# Duplicate entries or links don't seem to have a noticeable effect
# Return the system generated by the bodies and springs
def parse(text, *, friction = 0.2, repulsion = 0.1, spring_length = 0.25, spring_constant = 1, damping = 0.1, radius = 8, attraction = 0.01):

    bodyNames = set()
    bodies = list()
    springs = list()

    i = 0

    # Add all bodies
    entries = text.split("\n\n")
    for entry in entries:
        lines = entry.splitlines()
        headName = lines[0]

        if headName not in bodyNames:
            head = Physics.Body((math.cos(i), math.sin(i)), radius, label=headName)
            i += 1
            bodyNames.add(headName)
            bodies.append(head)
        else:
            head = find_body_by_name(bodies, headName)


        # Add springs to all dependencies, adding dependency nodes as necessary
        for line in lines[1:]:
            tailName = line[1:].lstrip() # Skip past leading dash

            if tailName not in bodyNames:
                tail = Physics.Body((math.cos(i), math.sin(i)), radius, label=tailName)
                i += 1
                bodyNames.add(tailName)
                bodies.append(tail)
            else:
                tail = find_body_by_name(bodies, tailName)

            print(f"Spring between {headName} and {tailName}")
            springs.append(Physics.Spring((head, tail), spring_length, spring_constant, damping))
    
    # Generate and return the system
    system = Physics.System(bodies, springs)
    system.friction_coefficient = friction
    system.repulsion_coefficient = repulsion
    system.attraction_coefficient = attraction
    return system
