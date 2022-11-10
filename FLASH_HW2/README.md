# MRI - HW2

In this homework, we will discuss three topics.

* Mxy and Mz
* The angle of maximum brightness between two tissues
* The subcortical volumes and Correlation

## Mxy and Mz

Simulate the timing of $M_z$ and $M_{xy}$.

There are two states in the timing:

* Excitation
* Relaxation

### **Excitation**

$M_{z}=Mz*cos\alpha$

$M_{xy}=Mz*sin\alpha$

### **Relaxation**

$M_{z}=1+(M_z-1) \times e^{-\frac{TR}{T1}}$

$M_{xy}=M_{xy} \times e^{-\frac{TR}{T2^\ast}}$

### **Iteration**

After times of RF excitation, $M_z$ and $M_{xy}$ will be stable.

![M_z stable](images/HW2.1.1.jpg)

![M_xy stable](images/HW2.1.2.jpg)

## The angle of maximum brightness between two tissues

We have two tissues, that means there are two T1 value: **1000** and **1100** ms.

By the equation:

$M\propto(\frac{(1-e^{-TR/T1}) \times sin\alpha}{1-e^{-TR/T1} \times cos\alpha})\times e^{-TE/T2^\ast}$

We can use `difference of number two` to find the angle of maximum brightness between two tissues.

![maximum difference](images/HW2.2.jpg)

## The subcortical volumes and Correlation
