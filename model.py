from mip import Model, INTEGER, minimize, xsum, OptimizationStatus

class Modelo:
    def __init__(self):
        self.model=Model("Inventario")

    def setsParameters(self, sets: dict, parameters:dict):
        self.productos=sets['productos']
        self.tiendas=sets['tiendas']

        self.demandaProducto = parameters['DemandaProducto'] # Demanda  producto i en tienda j
        self.costoInventario = parameters['CostoInventario'] # Costo por almacenar producto i tienda j
        self.costoQuiebre = parameters['CostoQuiebre']       # Costo quiebre Stock producto i tienda j
        self.cantidadMin = parameters['CantidadMinima']     #CAntidad minima de producto i en tienda j
        self.produccionMax = parameters['ProduccionMaxima'] # produccion maxima producto i  
        self.alamcenajeTienda = parameters['almacenajeTienda'] # Cantidad máxima de prodcutos de la tienda j


    def variables(self):
        self.x = [[self.model.add_var(var_type=INTEGER, lb=0, name=f'Unidades producto {i} en tienda {j}')for j in self.tiendas] for i in self.productos]
        self.xMax = [[self.model.add_var(var_type=INTEGER, lb=0, name =f"Sobre Stock producto {i} tienda {j}") for j in self.tiendas] for i in self.productos]
        self.xMin = [[self.model.add_var(var_type=INTEGER, lb=0, name =f"Quiebre Stock producto {i} tienda {j}") for j in self.tiendas] for i in self.productos]

    def objetive(self):
        self.model.objective = minimize(
            xsum(self.xMax[i][j] * self.costoInventario[i][j] for i in self.productos for j in self.tiendas) + 
            xsum(self.xMin[i][j] * self.costoQuiebre
            [i][j] for i in self.productos for j in self.tiendas)
        )
        
    def constrains(self):
        # Relacion de variables
        for i in self.productos:
            for j in self.tiendas:
                self.model += self.x[i][j] + self.xMin[i][j] - self.xMax[i][j] == self.demandaProducto[i][j]

        # Satisfacer demanda minina
        for i in self.productos:
            for j in self.tiendas:
                self.model += self.x[i][j] >= self.cantidadMin[i][j]

        # Producción Máxima Total de todas las tienda - Suponemos q la fabrica central tiene un limite máximo de producción por producto
        for i in self.productos:
            self.model += xsum(self.x[i][j] for j in self.tiendas) <= self.produccionMax[i]

        # Cantidad máxima de productos totales q puede tener una tienda
        for j in self.tiendas:
            self.model += xsum(self.x[i][j] for i in self.productos) <= self.alamcenajeTienda[j]

    def run_model(self):
        status = self.model.optimize()

        print("#############################################")
        if status == OptimizationStatus.OPTIMAL:
            print('[OPTIMAL] optimal solution profit {} found'.format(self.model.objective_value))
        elif status == OptimizationStatus.FEASIBLE:
            print('[FEASIBLE]  sol.profit {} found, best possible: {}'.format(self.model.objective_value, self.model.objective_bound))
        elif status == OptimizationStatus.NO_SOLUTION_FOUND:
            print('[Not Found] no feasible solution found, lower bound is: {}'.format(self.model.objective_bound))

    def results(self):
        return self.x