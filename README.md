# WTA
Heuristic approach to weapon target assignment problem

### Adaptation of Genetic Algorithm to the Target-Weapon Assignment Problem

#### Chromosome Structure
In our designed chromosome structure, the first gene of the chromosome represents the first target. For example, a value of 4 in the first gene indicates that the fourth weapon is assigned to the first target. Sequentially, the first, second, third, and fourth targets are assigned the fourth, first, third, and second weapons, respectively. In the chromosome below, "W" stands for weapon and "T" stands for target.

```
[〖WT〗_41 〖WT〗_12 〖WT〗_33,〖WT〗_24 ]
[4,1,3,2]
```

#### Chromosome Creation
The initial function sets up the genetic algorithm by creating a pool of chromosomes of a specified size (`poolSize`). Each chromosome is an instance of the Chromosome class, and the Create function is called to generate these chromosomes. The created chromosomes are then added to a list called `thePool`.

The second function actually creates the chromosomes. During this process, control steps of the genetic algorithm are applied. If the number of targets is greater than the number of weapons, imaginary weapons with zero impact are added for the difference. Then, a number of weapons equal to the number of targets are randomly selected and added to the chromosome, and their fitness value is calculated.

**Pool Class Create Function**
- Repeat for the pool size:
  - Create a new chromosome object (from the Chromosome class)
  - Call the Create function to generate the chromosome
  - Add the created chromosome to `thePool`
  - (The Create function in the Pool class calls the Control and Fitness functions of the Chromosome class to generate the chromosome)

**Chromosome Class Create Function**
- Call the Control function
- Repeat for the number of targets:
  - Randomly select a weapon from the weapon list and assign it to a variable
  - Add the selected weapon to the chromosome list
  - If the selected weapon is in the weapon list, remove it from the list
- Calculate the fitness value

#### Crossover Operators
The algorithm includes six different crossover options, and a random selection will be made among these options. Unlike classical genetic algorithms, the crossover operation will be performed on a single chromosome to avoid assigning the same weapon to multiple targets.

**RightShift Crossover Operator**
**RightShift Function**
- Select a random point
- Determine a random length from the selected point
- Select a random shift amount
- Create an empty list for the target pieces
- Create a new chromosome object and take a copy of the current chromosome (crossed)
- Remove the piece from the chromosome from the selected point for the determined length and add it to the piece list
- Place the piece in the new chromosome according to the shift amount
- Remove used weapons from the weapon list in the new chromosome
- Return the new chromosome

Example: 
```
Point = 1
Ln = 2
Shift = 1

Initial Chromosome: [4, [1,3], 2]
Result: [4, 2, 1, 3]
```

**LeftShift Crossover Operator**
**LeftShift Function**
- Select a random point
- Determine a random length from the selected point
- Select a random shift amount
- Create an empty list for the target pieces
- Create a new chromosome object and take a copy of the current chromosome (crossed)
- Remove the piece from the chromosome from the selected point for the determined length and add it to the piece list
- Place the piece in the new chromosome according to the shift amount
- Remove used weapons from the weapon list in the new chromosome
- Return the new chromosome

Example: 
```
Point = 1
Ln = 2
Shift = 1

Initial Chromosome: [4, [1,3], 2]
Result: [1, 3, 4, 2]
```

**ReverseChromosome Crossover Operator**
**ReverseChromosome Function**
- Create a new chromosome object and take a copy of the current chromosome (crossed)
- Reverse the copied chromosome
- Remove used weapons from the weapon list in the reversed chromosome
- Return the reversed chromosome

Example: 
```
Initial Chromosome: [4, 1, 3, 2]
Result: [2, 3, 1, 4]
```

**ReversePiece Crossover Operator**
**ReversePiece Function**
- Select a random point
- Determine a random length from the selected point
- Create a new chromosome object and take a copy of the current chromosome (crossed)
- Reverse the piece from the selected point for the determined length in the current chromosome
- Remove used weapons from the weapon list in the reversed piece
- Place the reversed piece in the same position in the current chromosome
- Return the new chromosome

Example: 
```
Point = 1
Ln = 2

Initial Chromosome: [4, [1,3], 2]
Result: [4, 3, 1, 2]
```

**SwapPieces Crossover Operator**
**SwapPieces Function**
- Select a random point, at least 1 and at most one less than the number of targets
- Determine a random length from the selected point
- Create a new chromosome object and take a copy of the current chromosome (crossed)
- Divide the current chromosome into three parts: head, mid, and tail
- Reassemble the parts in the new chromosome by swapping them
- Remove used weapons from the weapon list in the new chromosome
- Return the new chromosome

Example: 
```
For the middle piece:
Point = 1
Ln = 2

Initial Chromosome: [[4], [1,3], [2]]
Result: [2, 1, 3, 4]
```

**ReverseHeadAndTail Crossover Operator**
**ReverseHeadAndTail Function**
- Select a random point, at least 1 and at most one less than the number of targets
- Determine a random length from the selected point
- Create a new chromosome object and take a copy of the current chromosome (crossed)
- Divide the current chromosome into three parts: head, mid, and tail
- Reverse the head and tail while leaving the mid part unchanged
- Reassemble the parts in the new chromosome
- Remove used weapons from the weapon list in the new chromosome
- Return the new chromosome

Example: 
```
For the middle piece:
Point = 2
Ln = 2

Initial Chromosome: [[4, 1], [3, 2], [5, 6]]
Result: [1, 4, 3, 2, 6, 5]
```

#### Mutation Operator
The mutation operator "Mutation" used in target-weapon assignment increases diversity.

**Mutation Function**
- Generate a random value to check against the mutation rate
  - If it is less than or equal to the mutation rate:
    - Select a random target point
    - If there are still weapons in the weapon list:
      - Select a new weapon from the list to replace the current weapon at the target point
      - Place the new weapon at the target point and add the old weapon back to the list
    - If the number of weapons is less than or equal to the number of targets:
      - Randomly select two different target indices
      - Swap the weapons at the selected target indices

Examples: 
```
[4, 1, 3, 2]
If number of weapons ≤ number of targets: [4, 2, 3, 1]
Otherwise: [4, 5, 3, 2]
```

#### Selection Operator
In the used algorithm, the selection process is performed based on the total fitness value. Typically, in classic genetic algorithms, selection is done using methods like roulette wheel or tournament selection. In this problem, the roulette wheel is used for selection.

During selection, the fitness value of each chromosome is compared to the total fitness value, and the selection probability of each chromosome is calculated by dividing its fitness by the total fitness. A random number is then chosen, and the chromosome corresponding to this number is added to the new generation. This process repeats until the new generation pool is filled. The randomness in selection prevents the algorithm from getting stuck in local optima by sometimes eliminating even the best chromosome from the pool.

**Selection Function**
- Calculate the total fitness:
  - Initialize `total_fitness` to 0
  - Add the fitness of each chromosome to `total_fitness`
- Calculate fitness probabilities:
  - Create an empty `probabilities` list
  - For each chromosome:
    - Calculate its selection probability (fitness / total_fitness)
    - Add this probability to the `probabilities` list
- Determine selected chromosomes:
  - Create an empty `selected_chromosomes` list
  - Repeat for the pool size:
    - Generate a random number between 0 and 1 (`rand`)
    - Initialize `cumulative_prob` to 0
    - For each chromosome's probability:
      - Add to `cumulative_prob`
      - If `rand` is less than or equal to `cumulative_prob`:
        - Add the chromosome to `selected_chromosomes`
        - Break the loop
- Update `thePool` with `selected_chromosomes`
- Set a temporary list to empty

#### Finding the Best Chromosome Operator
Even if some chromosomes are eliminated during the selection process, the best chromosome in the pool will be retained in memory.

**FindBest Function**
- Set `theBest` to the last element in `self.theBest` list
- Initialize `b` to False

- For each `i` in `self.thePool`:
  - If `i.fitness`

 is greater than `theBest.fitness`:
    - `b` becomes True
    - Append `i` to `self.theBest`

- If `b` is False, append the last element in `self.theBest` to `self.theBest`

- Set the number of iterations to the last value of `self.theBest`

- ### Optimization of Operators

The `OperatorsOptimization` code utilizes a genetic algorithm-based approach to optimize parameters such as the number of iterations, pool size, and mutation rate for a given problem set.

#### WtaProblem Class

Each instance of this class represents the target-weapon assignment problem. To solve this problem, appropriate parameters must be defined: pool size, number of iterations, and mutation rate. The `WtaProblem` class solves the problem with different parameters and returns the best fitness value. The best solution and the parameters used for solving the problem are stored in memory.

#### OperatorsChromosome Class

Each instance of this class contains the parameters required to solve the target-weapon assignment problem. These parameters are defined as genes within the chromosomes. Chromosomes are randomly generated using the binary system. With the parameters in the generated chromosome, the target-weapon assignment problem is solved. The obtained value is the fitness value of this chromosome.

**Create Function:**
- Loop 21 times:
  - Append `random.randint(0, 1)` to `self.chromosome`
  - Call `Fitness()`

The first 7 genes of the chromosome represent the pool size, the genes from 7 to 14 represent the number of iterations, and the genes from 14 to 21 represent the mutation rate. The use of the binary system allows assigning many different values to the parameters, enhancing the efficiency of the crossover and mutation operators.

#### OperatorsPool Class

The `OperatorsPool` class manages and processes the chromosomes in the pool. This class applies genetic operators such as crossover and mutation and generates new chromosomes.

**__init__ Function:**
- Initializes the operator pool. The starting parameters (weapon, target, pool size, mutation rate, etc.) are defined. A "dummy" Operator Chromosome is created and set as the best.

**Create Function:**
- Adds random chromosomes to the pool. Each chromosome represents an operator combination to reach the target.

**Process Function:**
- Performs the main operations, including crossover, mutation, fitness calculation, merging, finding the best chromosome, and selection.

**Crossover Function:**
- Crosses the chromosomes in the pool, exchanging genetic material and creating new child chromosomes.

**Mutation Function:**
- Mutates the child chromosomes based on the mutation rate obtained from the crossover.

**ChildrenFitness Function:**
- Calculates the fitness values of the child chromosomes.

**Merge Function:**
- Adds the child chromosomes to the pool.

**Selection Function:**
- Performs selection based on the fitness values of the chromosomes in the pool, retaining the most suitable chromosomes.

When a round of the `Process` function is called, the new generation of chromosomes in the pool is created and the most suitable ones are selected. These steps are repeated, gradually determining the best operator combination.

In summary, the genetic algorithm designed for the target-weapon assignment problem works by encoding each solution as a chromosome, performing crossover and mutation operations to explore the search space, and using selection operators to retain the best solutions. The algorithm's robustness is enhanced by introducing diversity through various crossover methods and ensuring the best solutions are kept in memory.
