import pyideem
import numpy as np
from qiskit import QuantumCircuit

def pred_qasm(parameters):

  qasm_file = "./svm.qasm"
  
  with open(qasm_file, "r") as file:
      qasm_content = file.read()
  
  # 2. Замена параметров в содержимом QASM-файла
  for param, value in parameters.items():
      # Заменяем все вхождения параметра на его числовое значение
      qasm_content = qasm_content.replace(param, str(value))
  
  # 3. Сохранение нового QASM-файла с заменёнными параметрами
  temp_qasm_file = "./temp_qasm.qasm"
  with open(temp_qasm_file, "w") as file:
      file.write(qasm_content)
  
  # 4. Загрузка изменённого QASM-файла
  qc = pyideem.QuantumCircuit.loadQASMFile(temp_qasm_file)
  
  # Инициализация бэкенда для 2-кубитной схемы
  backend = pyideem.StateVector(2)
  
  # Выполнение схемы с 10 запусков
  result = qc.execute(5000, backend, noise_cfg=None, return_memory=True)
  
  counts = result.counts
  
  predicted_bits = max(counts, key=counts.get)
  
  bit_to_class = {
      '00': 0,
      '01': 0,
      '10': 1,
      '11': 1
  }
  
  predicted_class = bit_to_class[predicted_bits]
  print(predicted_class,predicted_bits)
  return(predicted_class)

theta = np.array([ 0.39248135, -0.48051543,  1.14371136, -0.6895156 ,  0.8201862 , 0.24864091,  0.79524104,  0.22269079])
x_test = np.array([[0.56820418, 0.43179582],
       [0.08532772, 0.91467228],
       [0.11201196, 0.88798804],
       [0.01031783, 0.98968217],
       [0.67824883, 0.32175117],
       [0.31239956, 0.68760044],
       [0.6841996 , 0.3158004 ],
       [0.41435187, 0.58564813],
       [0.39608468, 0.60391532],
       [0.61938205, 0.38061795],
       [0.65794036, 0.34205964],
       [0.12091184, 0.87908816],
       [0.50058409, 0.49941591],
       [0.85154292, 0.14845708],
       [0.12088576, 0.87911424],
       [0.74979508, 0.25020492],
       [0.55667997, 0.44332003],
       [0.93904937, 0.06095063],
       [0.21934802, 0.78065198],
       [0.6897127 , 0.3102873 ],
       [0.61612724, 0.38387276],
       [0.28802756, 0.71197244],
       [0.32171474, 0.67828526],
       [0.70942158, 0.29057842],
       [0.5438924 , 0.4561076 ],
       [0.08123323, 0.91876677],
       [0.71031475, 0.28968525],
       [0.71679241, 0.28320759],
       [0.27238911, 0.72761089],
       [0.38105026, 0.61894974],
       [0.11940621, 0.88059379],
       [0.88316991, 0.11683009],
       [0.11940699, 0.88059301],
       [0.1905123 , 0.8094877 ],
       [0.40916204, 0.59083796],
       [0.17640481, 0.82359519],
       [0.20547462, 0.79452538],
       [0.43971254, 0.56028746],
       [0.0123569 , 0.9876431 ],
       [0.37897041, 0.62102959],
       [0.03882203, 0.96117797],
       [0.49057581, 0.50942419]])

y_test = np.array([0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1,
       1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0])

accuracy = 0
for i in range(len(y_test)):
  parameters = {
        "x0": x_test[i][0], # признаки
        "x1": x_test[i][1], # признаки
        "θ0": theta[0],
        "θ1": theta[1],
        "θ2": theta[2], # обучаемы углы
        "θ3": theta[3],
        "θ4": theta[4],
        "θ5": theta[5],
        "θ6": theta[6],
        "θ7": theta[7]
    }
  # print(x_test[i][0])
  pred = pred_qasm(parameters)
  if pred == y_test[i]:
      accuracy += 1
print(accuracy/len(y_test))