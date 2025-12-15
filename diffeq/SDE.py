import diffeq.utils.vectors as _ve
import random


class integrator:
    def __init__(self, dt, inside_iterations=None):
        self.dt = dt
        self.ii = int(1/dt) if inside_iterations is None else inside_iterations

    def step(self, x, dx_dt):
        raise NotImplementedError

    def integrate(self, x, dx_dt):
        for _ in range(self.ii):
            x = self.step(x, dx_dt)
        return x


class euler_integrator(integrator):
    def step(self, x, dx_dt):
        return x + dx_dt(x)*self.dt


class rk4_integrator(integrator):
    def step(self, x, dx_dt):
        k1 = dx_dt(x)
        k2 = dx_dt(x + 0.5 * k1 * self.dt)
        k3 = dx_dt(x + 0.5 * k2 * self.dt)
        k4 = dx_dt(x + k3 * self.dt)
        return x + (k1 + 2*k2 + 2*k3 + k4) * (self.dt / 6)


class system:
    def __init__(self, ds_dt: _ve.vector_function, solver, initials: _ve.vector = None):
        if initials is None:
            initials = _ve.vector({i: random.gauss() for i in ds_dt.out_axes})
        self.state: _ve.vector = initials
        self.ds_dt = ds_dt
        self.solver: 'integrator' = solver

    def update(self):
        self.state = self.solver.integrate(self.state, self.ds_dt)

    def run(self, t_end, t_start=0):
        t = t_start
        history = {
            's': _ve.vector({k:[] for k in self.state.keys()}),
            't': []
        }
        while True:
            history['s'].apply_vector_operation(self.state, lambda x, y: x.append(y))
            history['t'].append(t)
            self.update()
            t += self.solver.dt*self.solver.ii
            if t >= t_end:
                break
        return history
