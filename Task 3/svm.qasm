OPENQASM 2.0;
include "qelib1.inc";

// Определение регистров
qreg q[2];
creg c[2];

// ZZFeatureMap
u2(0,pi) q[0];
u2(0,pi) q[1];
u1(2*x0) q[0];
u1(2*x1) q[1];
cx q[0],q[1];
u1(2*x0*x1) q[1];
cx q[0],q[1];

// RealAmplitudes Ansatz
u3(θ0,0,0) q[0];
u3(θ1,0,0) q[1];
cx q[0],q[1];
u3(θ2,0,0) q[0];
u3(θ3,0,0) q[1];
cx q[0],q[1];
u3(θ4,0,0) q[0];
u3(θ5,0,0) q[1];
cx q[0],q[1];
u3(θ6,0,0) q[0];
u3(θ7,0,0) q[1];
// --- Измерения ---
measure q[0] -> c[0];
measure q[1] -> c[1];