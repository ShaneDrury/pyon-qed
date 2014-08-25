#!/usr/local/bin/MathematicaScript -runfirst "$TopDirectory=\"/usr/local/Wolfram/Mathematica/8.0\"" -script

q1  = ToExpression[$ScriptCommandLine[[2]]];
q3  = ToExpression[$ScriptCommandLine[[3]]];
q4  = ToExpression[$ScriptCommandLine[[4]]];
q5  = ToExpression[$ScriptCommandLine[[5]]];
q6  = ToExpression[$ScriptCommandLine[[6]]];
m1  = ToExpression[$ScriptCommandLine[[7]]];
m3  = ToExpression[$ScriptCommandLine[[8]]];
m4  = ToExpression[$ScriptCommandLine[[9]]];
m5  = ToExpression[$ScriptCommandLine[[10]]];
m6  = ToExpression[$ScriptCommandLine[[11]]];
B0  = ToExpression[$ScriptCommandLine[[12]]];
mres = ToExpression[$ScriptCommandLine[[13]]];
L  = ToExpression[$ScriptCommandLine[[14]]];

(* ::Input:: *)
I1[\[Chi]_]:=1/(16\[Pi]^2) \[Chi]*Log[\[Chi]/\[Mu]^2];


(* ::Input:: *)
I2[\[Chi]_]:=1/(16\[Pi]^2) (Log[\[Chi]/\[Mu]^2]+1);


(* ::Input:: *)
I0[\[Chi]_]:=0;


(* ::Input:: *)
J[\[Chi]_]:=1/(16\[Pi]^2) (Log[\[Chi]/\[Mu]^2]-1);


(* ::Input:: *)
K[\[Chi]_]:=-(1/(2*16\[Pi]^2))\[Chi]*Log[\[Chi]/\[Mu]^2];


(* ::Input:: *)
JIR[\[Chi]_]:=0;


(* ::Input:: *)
KIR[\[Chi]_]:=0;


(* ::Input:: *)
dI1[\[Chi]_,L_,\[CapitalLambda]l_,\[CapitalLambda]h_]:=1/(4\[Pi] L^2) Re[NIntegrate[1/\[Lambda]^2*Exp[-((L^2 \[Chi] \[Lambda])/(4\[Pi]))](\[Lambda]^(3/2)-S[\[Lambda]]),{\[Lambda],\[CapitalLambda]l,\[CapitalLambda]h}]];


(* ::Input:: *)
dI2[\[Chi]_,L_,\[CapitalLambda]l_,\[CapitalLambda]h_]:=-(1/(16\[Pi]^2))Re[NIntegrate[1/\[Lambda]*Exp[-((L^2 \[Chi] \[Lambda])/(4\[Pi]))](\[Lambda]^(3/2)-S[\[Lambda]]),{\[Lambda],\[CapitalLambda]l,\[CapitalLambda]h}]];


(* ::Input:: *)
dI0[\[Chi]_,L_,\[CapitalLambda]l_,\[CapitalLambda]h_]:=-(1/(4\[Pi] L^2))Re[NIntegrate[1/\[Lambda]^2 S[\[Lambda]],{\[Lambda],\[CapitalLambda]l,\[CapitalLambda]h}]];

(* ::Input:: *)
Kap[\[CapitalLambda]l_,\[CapitalLambda]h_]:=Re[NIntegrate[1/\[Lambda]^2 S[\[Lambda]],{\[Lambda],\[CapitalLambda]l,\[CapitalLambda]h}]];


(* ::Input:: *)
dJ[\[Chi]_,L_,\[CapitalLambda]l_,\[CapitalLambda]h_]:=1/(16\[Pi]*L Sqrt[\[Chi]]) Re[NIntegrate[1/\[Lambda]^(3/2)*Erf[L Sqrt[(\[Chi] \[Lambda])/(4\[Pi])]]*S[\[Lambda]],{\[Lambda],\[CapitalLambda]l,\[CapitalLambda]h}]];


(* ::Input:: *)
dK[\[Chi]_,L_,\[CapitalLambda]l_,\[CapitalLambda]h_]:=-(1/(8\[Pi]*L^2))Re[NIntegrate[1/\[Lambda]^2*(1-Exp[-((L^2 \[Chi] \[Lambda])/(4\[Pi]))])*S[\[Lambda]],{\[Lambda],\[CapitalLambda]l,\[CapitalLambda]h}]];


(* ::Input:: *)
dJIR[\[Chi]_,L_,\[CapitalLambda]l_,\[CapitalLambda]h_]:=-(\[Pi]/(16\[Pi]^2 L Sqrt[\[Chi]]))Re[NIntegrate[1/\[Lambda]^(3/2) S[\[Lambda]],{\[Lambda],\[CapitalLambda]l,\[CapitalLambda]h}]];


(* ::Input:: *)
dKIR[\[Chi]_,L_,\[CapitalLambda]l_,\[CapitalLambda]h_]:=-(1/(4\[Pi] L^2 Sqrt[\[Chi]]))Re[NIntegrate[1/\[Lambda]^2 S[\[Lambda]],{\[Lambda],\[CapitalLambda]l,\[CapitalLambda]h}]];


(* ::Input:: *)
\[Theta]3=\!\( 
\*SubsuperscriptBox[\(\[Sum]\), \(i = \(-\[Infinity]\)\), \(\[Infinity]\)]\(Exp[\(-
\*FractionBox[\(\[Pi]\), \(\[Lambda]\)]\) \(( 
\*SuperscriptBox[\(i\), \(2\)])\)]\)\);


(* ::Input:: *)
S[\[Lambda]_]:=-(\[Theta]3^3-1-\[Lambda]^(3/2));

(* PION: This is the correction to the terms proportional to C / F^4 (line 2 of the FV correction in Rans paper)*)
FV2[\[Chi]1_,\[Chi]3_,\[Chi]4_,\[Chi]5_,\[Chi]6_,q1_,q3_,q4_,q5_,q6_,L_,\[CapitalLambda]l_,\[CapitalLambda]h_]:=(dI1[(\[Chi]1+\[Chi]4)/2,L,\[CapitalLambda]l,\[CapitalLambda]h]*(q1-q4)*(q1-q3)-dI1[(\[Chi]3+\[Chi]4)/2,L,\[CapitalLambda]l,\[CapitalLambda]h]*(q3-q4)*(q1-q3))+(dI1[(\[Chi]1+\[Chi]5)/2,L,\[CapitalLambda]l,\[CapitalLambda]h]*(q1-q5)*(q1-q3)-dI1[(\[Chi]3+\[Chi]5)/2,L,\[CapitalLambda]l,\[CapitalLambda]h]*(q3-q5)*(q1-q3))

(* PION: This is the correction to the terms proportional to e^2 but not C / F^4 (line 1 of the FV correction in Rans paper) *)
FV3[\[Chi]1_,\[Chi]3_,f\[Chi]4_,\[Chi]5_,\[Chi]6_,q1_,q3_,q4_,q5_,q6_,L_,\[CapitalLambda]l_,\[CapitalLambda]h_]:=-(q1-q3)^2(4 (\[Chi]1+\[Chi]3)/2 dJ[(\[Chi]1+\[Chi]3)/2,L,\[CapitalLambda]l,\[CapitalLambda]h]+2dK[(\[Chi]1+\[Chi]3)/2,L,\[CapitalLambda]l,\[CapitalLambda]h])+3(q1-q3)^2*dI0[0,L,\[CapitalLambda]l,\[CapitalLambda]h];

(* KAON *)
FVKAON1[\[Chi]1_,\[Chi]3_,\[Chi]4_,\[Chi]5_,\[Chi]6_,q1_,q3_,q4_,q5_,q6_,L_,\[CapitalLambda]l_,\[CapitalLambda]h_]:=(dI1[(\[Chi]1+\[Chi]4)/2,L,\[CapitalLambda]l,\[CapitalLambda]h]+dI1[(\[Chi]1+\[Chi]5)/2,L,\[CapitalLambda]l,\[CapitalLambda]h])

(* Kaon2 *)
FVKAON2[\[Chi]1_,\[Chi]3_,\[Chi]4_,\[Chi]5_,\[Chi]6_,q1_,q3_,q4_,q5_,q6_,L_,\[CapitalLambda]l_,\[CapitalLambda]h_]:=(3.0 * Kap[\[CapitalLambda]l,\[CapitalLambda]h] / 4.0 / \[Pi] / L / L + dK[(\[Chi]1+\[Chi]3)/2,L,\[CapitalLambda]l,\[CapitalLambda]h] + 4.0 * (\[Chi]1+\[Chi]3)/2 * dJ[(\[Chi]1+\[Chi]3)/2,L,\[CapitalLambda]l,\[CapitalLambda]h])



EM=0.30286`;
\[Chi]1=2B0*mu;\[Chi]3=2B0*md;\[Chi]4=2B0*mu;\[Chi]5=2B0*md;\[Chi]6=2B0*ms;
Print[Quiet[2*FV2[2 B0*(m1+mres),2 B0*(m3+mres),2 B0*(m4+mres),2 B0*(m5+mres),2 B0*(m6+mres),EM * q1/3.0,EM * q3/3.0,EM * q4/3.0,EM * q5/3.0,EM * q6/3.0,24,10^-4,10^5]]]
Print[Quiet[FV3[2 B0*(m1+mres),2 B0*(m3+mres),2 B0*(m4+mres),2 B0*(m5+mres),2 B0*(m6+mres),EM * q1/3.0,EM * q3/3.0,EM * q4/3.0,EM * q5/3.0,EM * q6/3.0,24,10^-4,10^5]]]
Print[Quiet[FVKAON1[2 B0*(m1+mres),2 B0*(m3+mres),2 B0*(m4+mres),2 B0*(m5+mres),2 B0*(m6+mres),EM * q1/3.0,EM * q3/3.0,EM * q4/3.0,EM * q5/3.0,EM * q6/3.0,24,10^-4,10^5]]]
Print[Quiet[FVKAON2[2 B0*(m1+mres),2 B0*(m3+mres),2 B0*(m4+mres),2 B0*(m5+mres),2 B0*(m6+mres),EM * q1/3.0,EM * q3/3.0,EM * q4/3.0,EM * q5/3.0,EM * q6/3.0,24,10^-4,10^5]]]




