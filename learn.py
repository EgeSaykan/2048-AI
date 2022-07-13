import os
import neat as nt
import game2048


def activateGenome(events, gnome, gnomeMatrix):
    output = gnome.activate((gnomeMatrix[0][0], gnomeMatrix[0][1], gnomeMatrix[0][2], gnomeMatrix[0][3], gnomeMatrix[1][0], gnomeMatrix[1][1], gnomeMatrix[1][2], gnomeMatrix[1][3], gnomeMatrix[2][0], gnomeMatrix[2][1], gnomeMatrix[2][2], gnomeMatrix[2][3], gnomeMatrix[3][0], gnomeMatrix[3][1], gnomeMatrix[3][2], gnomeMatrix[3][3]))
    biggest = 0
    for i in range(4):
        if output[i] > output[biggest]: biggest = i
    direction = ""
    for event in events:
        if biggest == 0:
            direction = "LEFT"
        elif biggest == 1:
            direction = "RIGHT"
        elif biggest == 2:
            direction = "UP"
        elif biggest == 3:
            direction = "DOWN"
    return direction


def returnTrue(*arg): return True

def eval_genomes(genomes, config):

    nets = []
    grids = []
    ge = []
    for genome_id, genome in genomes:
        genome.fitness = 0  # start with fitness level of 0
        net = nt.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        grids.append(game2048.Game2048())
        ge.append(genome)
    game2048.GameLoop2048(activateGenome, returnTrue, grids, nets, ge)


# runs the nt algorithm to train a neural network to play flappy bird.
# :param config_file: location of config file
def run(config_file):
    config = nt.config.Config(nt.DefaultGenome, nt.DefaultReproduction,
                         nt.DefaultSpeciesSet, nt.DefaultStagnation,
                         config_file)

    population = nt.Population(config)

    # Create the population, which is the top-level object for a nt run.
    population = nt.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    population.add_reporter(nt.StdOutReporter(True))
    stats = nt.StatisticsReporter()
    population.add_reporter(stats)
    #population.add_reporter(nt.Checkpointer(5))

    # Run for up to 50 generations.
    winner = population.run(eval_genomes, 500)

    # show final stats
    print('\nBest genome:\n{!s}'.format(winner))

if __name__ == '__main__':
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    run(config_path)