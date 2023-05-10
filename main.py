import random
import numpy as np


class DietPSO:
    # Sınıfın yapıcı (constructor) metodu tanımlanıyor ve sınıfın özellikleri belirtiyoruz
    def __init__(self, population_size, n_iterations, n_variables, lower_bounds, upper_bounds, macronutrient_ratios,
                 fitness_func):
        self.population_size = population_size
        self.n_iterations = n_iterations
        self.n_variables = n_variables
        self.lower_bounds = lower_bounds
        self.upper_bounds = upper_bounds
        self.macronutrient_ratios = macronutrient_ratios
        self.fitness_func = fitness_func
        self.global_best_position = None
        self.global_best_fitness = float('inf')
        self.population = self.initialize_population()

    # Popülasyonu oluşturmak için kullanılacak metot tanımlıyoruz
    def initialize_population(self):
        population = []
        for i in range(self.population_size):
            individual = {'position': np.random.uniform(self.lower_bounds, self.upper_bounds, self.n_variables),
                          'velocity': np.zeros(self.n_variables),
                          'personal_best_position': None, #değeri henüz belirlenmediği için None
                          'personal_best_fitness': float('inf')}
            population.append(individual)
        return population

    # PSO algoritmasının çalıştırılacağı metot tanımlıyoruz
    def run(self):
        # her yineleme için popülasyondaki her bir parçacığın uygunluğunu değerlendiriyoruz.
        for i in range(self.n_iterations):
            for j in range(self.population_size):
                individual = self.population[j]
                fitness = self.fitness_func(individual['position'])
                # Bireyin kişisel en iyi durumunu güncelliyoruz
                if fitness < individual['personal_best_fitness']:
                    individual['personal_best_fitness'] = fitness
                    individual['personal_best_position'] = individual['position'].copy()
                # Global en iyi durumunu güncelliyoruz
                if fitness < self.global_best_fitness:
                    self.global_best_fitness = fitness
                    self.global_best_position = individual['position'].copy()
                # PSO algoritmasının denklemi uygulanıyoruz
                w = 0.729    # Ağırlık faktörü(parçacık hızı)
                c1 = 1.49445 # Bireysel öğrenme faktörü
                c2 = 1.49445  # Sürü öğrenme faktörü
                r1 = np.random.rand(self.n_variables)
                r2 = np.random.rand(self.n_variables)
                 #mevcut hızın bir kısmı koruyoruz aynı zamanda bireysel ve küresel en iyi pozisyonlara doğru harekete bakıyoruz
                individual['velocity'] = (w * individual['velocity'] +
                                          c1 * r1 * (individual['personal_best_position'] - individual['position']) +
                                          c2 * r2 * (self.global_best_position - individual['position']))

                # Sınırları aşmaması için hızı kontrol ediyoruz
                individual['velocity'] = np.minimum(individual['velocity'], self.upper_bounds - individual['position'])
                individual['velocity'] = np.maximum(individual['velocity'], self.lower_bounds - individual['position'])
                # Bireyin pozisyonunu güncelle
                individual['position'] += individual['velocity']
                # Sınırları aşmaması için pozisyonu kontrol ediyoruz
                individual['position'] = np.minimum(individual['position'], self.upper_bounds)
                individual['position'] = np.maximum(individual['position'], self.lower_bounds)

    # En iyi çözümü döndüren metot tanımlıyoruz
    def get_best_solution(self):
        return self.global_best_position


def calculate_fitness(position):
    # Diyetteki makrobesin oranları ile istenen makrobesin oranları arasındaki farkı hesaplayan fitness fonksiyonu
    # Bu değeri en aza indirmek istiyoruz
    carb_ratio, protein_ratio, fat_ratio = calculate_macronutrient_ratios(position)
    return abs(carb_ratio - macronutrient_ratios[0]) + abs(protein_ratio - macronutrient_ratios[1]) + abs(
        fat_ratio - macronutrient_ratios[2])

# Pozisyondaki diyet bileşenlerinin karbonhidrat, protein ve yağ oranlarını hesaplıyoruz.
def calculate_macronutrient_ratios(position):
    carb_ratio = np.sum(position[:n_carbs]) / np.sum(position)
    protein_ratio = np.sum(position[n_carbs:n_carbs + n_proteins]) / np.sum(position)
    fat_ratio = np.sum(position[n_carbs + n_proteins:]) / np.sum(position)
    return carb_ratio, protein_ratio, fat_ratio


n_carbs = 1
n_proteins = 1
n_fats = 1
n_items = n_carbs + n_proteins + n_fats
macronutrient_ratios = [0.5, 0.3, 0.2]  # # İstenen makrobesinin %lik karbonhidrat, protein, yağ oranı
lower_bounds = np.ones(n_items) * 1 # Gıda maddesinin miktarına ilişkin alt sınırlar
upper_bounds = np.ones(n_items) * 500  # Gıda maddesinin miktarına ilişkin üst sınırlar
population_size = 100
n_iterations = 5

pso = DietPSO(population_size, n_iterations, n_items, lower_bounds, upper_bounds, macronutrient_ratios,
              calculate_fitness)
pso.run()
best_solution = pso.get_best_solution()
print(best_solution)