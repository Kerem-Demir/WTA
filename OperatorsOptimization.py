import WTA
import random

class WtaProblem:
    def __init__(self, weapon, target, poolSize, iteration, mutationRate):
        self.weapon = weapon
        self.target = target
        self.poolSize = poolSize
        self.mutationRate = mutationRate
        self.iteration = iteration
        self.fitness = -1
        self.object = WTA.Pool(self.poolSize, self.target, self.weapon, self.mutationRate)
        dummy = WTA.Pool(self.poolSize, self.mutationRate, self.target, self.weapon)
        dummy.theBest[-1].fitness = 0
        self.theBest = [dummy]


    def Process(self):
        self.Run()
        self.FindBest()

    def Create(self):
        self.object.Create()

    def Run(self):
        print(self.iteration, " iterasyon sayısı ve ", self.poolSize, " poolsize ve ", self.mutationRate, "mutasyon oranı ile fitness değeri hesaplanıyor...")
        for i in range(self.iteration):
            self.object.Process()
        self.fitness = self.object.theBest[-1].fitness
        print(self.fitness)


    def FindBest(self):
        theBest = self.theBest[-1]
        b = False

        if self.object.theBest[-1].fitness > theBest.theBest[-1].fitness:
            del theBest
            theBest = self.object
            theBest.chromosome = self.object.theBest[-1].chromosome
            theBest.fitness = self.object.theBest[-1].fitness
            b = True
        if (b):
            self.theBest.append(theBest)



class OperatorsPool():
    def __init__(self, weapon, target):
        self.weapon = weapon
        self.target = target
        self.poolSize = 10
        self.pool = []
        self.children = []
        self.mutationRate = 0.3
        dummy=OperatorsChromosome(self.weapon, self.target)
        dummy.fitness=0
        self.theBest=[dummy]

    def Process(self):
        self.Crossover()
        self.Mutation()
        self.ChildrenFitness()
        self.Merge()
        self.FindBest()
        self.Selection()

    def FindBest(self):
        theBest=self.theBest[-1]
        b=False
        for i in self.pool:
            if i.fitness>theBest.fitness:
                del theBest
                theBest= i
                theBest.chromosome=i.chromosome
                theBest.fitness=i.fitness
                b=True
        if (b):
            self.theBest.append(theBest)

    def Create(self):
        for _ in range(self.poolSize):
            chromosome = OperatorsChromosome(self.weapon, self.target)
            chromosome.Create()
            self.pool.append(chromosome)


    def Crossover(self):
        crossed1 = []
        crossed2 = []
        for i in range(len(self.pool)):
            if i % 2 == 0:
                crossed1 = self.pool[i]
            else :
                crossed2 = self.pool[i]

            if crossed1 and crossed2 :
                crossed1.crossed.append(crossed1.chromosome)
                crossed1.crossed.append(crossed2.chromosome)

                self.children.append(crossed1.Crossover()[0])
                self.children.append(crossed1.Crossover()[1])

                crossed1 = []
                crossed2 = []

    def Mutation(self):
        for i in self.children:
            if random.random() < self.mutationRate:
                i.Mutation()

    def ChildrenFitness(self):
        for i in self.children:
            i.Fitness()

    def Merge(self):
        for i in self.children:
            self.pool.append(i)

    def Selection(self):
        total_fitness = 0
        for i in self.pool:
            total_fitness += i.fitness


        probabilities = []
        for i in self.pool:
            prob = i.fitness / total_fitness
            probabilities.append(prob)


        selected_chromosomes = []
        for _ in range(self.poolSize):
            rand = random.random()
            cumulative_prob = 0
            for i, prob in enumerate(probabilities):
                cumulative_prob += prob
                if rand <= cumulative_prob:
                    selected_chromosomes.append(self.pool[i])
                    break
        self.pool = selected_chromosomes
        self.children = []




class OperatorsChromosome():
    def __init__(self, weapon, target):
        self.weapon = weapon
        self.target = target
        self.chromosome = []
        self.crossed = []
        self.fitness = -1
        self.theBestChromosome = []

    def Create(self):
        for _ in range(21):
            self.chromosome.append(random.randint(0, 1))
        self.Fitness()

    def Crossover(self):
        rnd = random.randint(0, 20)
        child1 = OperatorsChromosome(self.weapon, self.target)
        child2 = OperatorsChromosome(self.weapon, self.target)

        child1.chromosome = self.crossed[0][rnd:] + self.crossed[1][:rnd]
        child2.chromosome =  self.crossed[0][:rnd] + self.crossed[1][rnd:]

        return child1, child2


    def Mutation(self):
        rndVal = random.randint(0, 1)
        rndInd = random.randint(0,20)
        self.chromosome[rndInd] = rndVal

    def Decimal(self):
        poolSize = (int(''.join(map(str, self.chromosome[:7])), 2) +1)
        iteration = (int(''.join(map(str, self.chromosome[7:14])), 2) +1)
        mutationRate = (int(''.join(map(str, self.chromosome[14:20])), 2) + 1) /128

        return poolSize, iteration, mutationRate

    def Fitness(self):

        prob = WtaProblem(self.weapon, self.target, self.Decimal()[0], self.Decimal()[1], self.Decimal()[2])
        prob.Create()
        prob.Process()

        self.fitness = prob.theBest[-1].theBest[-1].fitness
        self.theBestChromosome = prob.theBest[-1].theBest[-1].chromosome

        del prob
