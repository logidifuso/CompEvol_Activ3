def rhh(size):
    """
    Create a population of size using ramped half and half (or sensible
    initialisation) and return.
    :param size: The size of the required population.
    :return: A full population of individuals.
    """
    # Calculate the range of depths to ramp individuals from.
    depths = range(params['BNF_GRAMMAR'].min_ramp + 1,
                   params['MAX_INIT_TREE_DEPTH']+1)
    population = []

    if size < 2:
        # If the population size is too small, can't use RHH initialisation.
        print("Error: population size too small for RHH initialisation.")
        print("Returning randomly built trees.")
        return [individual.Individual(sample_genome(), None)
                for _ in range(size)]

    elif not depths:
        # If we have no depths to ramp from, then params['MAX_INIT_DEPTH'] is
        # set too low for the specified grammar.
        s = "operators.initialisation.rhh\n" \
            "Error: Maximum initialisation depth too low for specified " \
            "grammar."
        raise Exception(s)

    else:
        if size % 2:
            # Population size is odd, need an even population for RHH
            # initialisation.
            size += 1
            print("Warning: Specified population size is odd, "
                  "RHH initialisation requires an even population size. "
                  "Incrementing population size by 1.")

        if size/2 < len(depths):
            # The population size is too small to fully cover all ramping
            # depths. Only ramp to the number of depths we can reach.
            depths = depths[:int(size/2)]

        # Calculate how many individuals are to be generated by each
        # initialisation method.
        times = int(floor((size/2)/len(depths)))
        remainder = int(size/2 - (times * len(depths)))

        # Iterate over depths.
        for depth in depths:
            # Iterate over number of required individuals per depth.
            for i in range(times):

                # Generate individual using "Grow"
                ind = generate_ind_tree(depth, "random")

                # Append individual to population
                population.append(ind)

                # Generate individual using "Full"
                ind = generate_ind_tree(depth, "full")

                # Append individual to population
                population.append(ind)

        if remainder:
            # The full "size" individuals were not generated. The population
            # will be completed with individuals of random depths.
            depths = list(depths)
            shuffle(depths)

        for i in range(remainder):
            depth = depths.pop()

            # Generate individual using "Grow"
            ind = generate_ind_tree(depth, "random")

            # Append individual to population
            population.append(ind)

            # Generate individual using "Full"
            ind = generate_ind_tree(depth, "full")

            # Append individual to population
            population.append(ind)

        return population
