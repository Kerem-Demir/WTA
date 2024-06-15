import random


class Pool:
    def __init__(self, poolSize, numberofTarget, numberofWeapon, mutationRate):
        self.thePool=[]
        self.poolSize = poolSize
        self.numberofTarget = numberofTarget
        self.numberofWeapon = numberofWeapon
        self.temporary=[]
        self.mutationRate= mutationRate
        dummy=Chromosome(self, self.mutationRate, self.numberofTarget, self.numberofWeapon)
        dummy.fitness=0
        self.theBest=[dummy]

    def Process(self):
        self.Crossover()
        self.Merge()
        self.FindBest()
        self.Selection()

    def Create(self):
        for _ in range(self.poolSize):
            chromosome = Chromosome(self.thePool, self.mutationRate, self.numberofTarget, self.numberofWeapon)
            chromosome.Create()
            self.thePool.append(chromosome)

    def FindBest(self):
        theBest=self.theBest[-1]
        b=False
        for i in self.thePool:
            if i.fitness>theBest.fitness:
                del theBest
                theBest=Chromosome(i.thePool, i.mutationRate, i.numberofTarget, i.numberofWeapon)
                theBest.chromosome=i.chromosome
                theBest.fitness=i.fitness
                b=True
        if (b):
            self.theBest.append(theBest)

    def Selection(self):
        total_fitness = 0
        for i in self.thePool:
            total_fitness += i.fitness


        probabilities = []
        for i in self.thePool:
            prob = i.fitness / total_fitness
            probabilities.append(prob)


        selected_chromosomes = []
        for _ in range(self.poolSize):
            rand = random.random()
            cumulative_prob = 0
            for i, prob in enumerate(probabilities):
                cumulative_prob += prob
                if rand <= cumulative_prob:
                    selected_chromosomes.append(self.thePool[i])
                    break
        self.thePool = selected_chromosomes
        self.temporary = []


    def Merge(self):
        for i in self.temporary:
            self.thePool.append(i)

    def Crossover(self):
        for i in self.thePool:
            self.temporary.append(i.Crossover())


class Chromosome:
    def __init__(self, pool, mutation, numberofTarget, numberofWeapon):
        self.thePool=pool
        self.chromosome=[]
        self.fitness=-1
        self.mutationRate=mutation
        self.numberofWeapon = numberofWeapon
        self.weaponList= list(range(1,self.numberofWeapon+1))
        self.numberofTarget= numberofTarget


    def Control(self):
        if self.numberofTarget > self.numberofWeapon:
            for i in range(self.numberofTarget - self.numberofWeapon):
                self.weaponList.append(0)

    def Create(self):
        self.Control()
        for i in range(self.numberofTarget):
            found = random.choice(self.weaponList)
            self.chromosome.append(found)
            if found in self.weaponList:
                self.weaponList.remove(found)
        self.Fitness()



    def Crossover(self):
        rnd = random.randint(1, 6)

        if rnd == 1:
            newChromosome = self.RightShift()
        elif rnd == 2:
            newChromosome = self.LeftShift()
        elif rnd == 3:
            newChromosome = self.ReverseChromosome()
        elif rnd == 4:
            newChromosome = self.ReversePiece()
        elif rnd == 5:
            newChromosome = self.SwapPieces()
        elif rnd == 6:
            newChromosome = self.ReverseHeadAndTail()


        newChromosome.Mutation()
        newChromosome.Fitness()

        return newChromosome


    def RightShift(self):

        point = random.randint(0, self.numberofTarget-1)
        ln = random.randint(1, self.numberofTarget - point)
        shift = random.randint(1, self.numberofTarget - 1)
        piece = []
        crossed = Chromosome(self.thePool, self.mutationRate, self.numberofTarget, self.numberofWeapon)
        crossed.chromosome = list(self.chromosome)


        for i in range(ln):
            piece.append(crossed.chromosome[point])
            crossed.chromosome.pop(point)

        for i in range(len(piece)):
            crossed.chromosome.insert((point + i + shift) % (len(crossed.chromosome) + ln), piece[i])

        for i in crossed.chromosome:
            if i in crossed.weaponList:
                crossed.weaponList.remove(i)
        return crossed

    def LeftShift(self):
        point = random.randint(0, self.numberofTarget-1)
        ln = random.randint(1, self.numberofTarget - point)
        shift = random.randint(1, self.numberofTarget - 1)
        piece = []
        crossed = Chromosome(self.thePool, self.mutationRate, self.numberofTarget, self.numberofWeapon)
        crossed.chromosome = list(self.chromosome)

        for i in range(ln):
            piece.append(crossed.chromosome[point])
            crossed.chromosome.pop(point)

        for i in range(len(piece)):
            crossed.chromosome.insert((point + i - shift) % (len(crossed.chromosome) + ln), piece[i])

        for i in crossed.chromosome:
            if i in crossed.weaponList:
                crossed.weaponList.remove(i)
        return crossed

    def ReverseChromosome(self):
        crossed = Chromosome(self.thePool, self.mutationRate, self.numberofTarget, self.numberofWeapon)
        crossed.chromosome = list(self.chromosome)
        crossed.chromosome.reverse()

        for i in crossed.chromosome:
            if i in crossed.weaponList:
                crossed.weaponList.remove(i)
        return crossed

    def ReversePiece(self):
        point = random.randint(0, self.numberofTarget -1)
        ln = random.randint(1, self.numberofTarget - point)
        crossed = Chromosome(self.thePool, self.mutationRate, self.numberofTarget, self.numberofWeapon)
        crossed.chromosome = list(self.chromosome)

        crossed.chromosome[point:point+ln+1] = crossed.chromosome[point:point+ln+1][::-1]

        for i in crossed.chromosome:
            if i in crossed.weaponList:
                crossed.weaponList.remove(i)
        return crossed

    def SwapPieces(self):
        point = random.randint(1, self.numberofTarget -1)
        ln = random.randint(1, self.numberofTarget - point)
        crossed = Chromosome(self.thePool, self.mutationRate, self.numberofTarget, self.numberofWeapon)
        crossed.chromosome = list(self.chromosome)

        head = crossed.chromosome[:point]
        mid = crossed.chromosome[point:point +ln]
        tail = crossed.chromosome[point + ln:]
        crossed.chromosome = tail +mid + head

        for i in crossed.chromosome:
            if i in crossed.weaponList:
                crossed.weaponList.remove(i)

        return crossed

    def ReverseHeadAndTail(self):
        point = random.randint(1, self.numberofTarget -1)
        ln = random.randint(1, self.numberofTarget - point)
        crossed = Chromosome(self.thePool, self.mutationRate, self.numberofTarget, self.numberofWeapon)
        crossed.chromosome = list(self.chromosome)

        head = crossed.chromosome[:point][::-1]
        mid = crossed.chromosome[point:point +ln]
        tail = crossed.chromosome[point + ln:][::-1]
        crossed.chromosome = head +mid + tail

        for i in crossed.chromosome:
            if i in crossed.weaponList:
                crossed.weaponList.remove(i)
        return crossed


    def Mutation(self):
        if random.random()<=self.mutationRate:
            point=random.randint(0,self.numberofTarget-1)
            if len(self.weaponList)>0:
                mt=random.choice(self.weaponList)
                self.weaponList.append(self.chromosome[point])
                self.chromosome[point]=mt
                self.weaponList.remove(mt)
            else:
                index1, index2 = random.sample(range(self.numberofTarget), 2)
                self.chromosome[index1], self.chromosome[index2] = self.chromosome[index2], self.chromosome[index1]



    def Fitness(self):

        for i, j in zip(self.chromosome, range(1, self.numberofTarget + 1)):
            self.fitness += i * j

