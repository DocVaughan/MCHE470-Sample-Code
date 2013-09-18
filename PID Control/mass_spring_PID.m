% this line allows running directly from the shell... probably leaved commented out
% #!/usr/local/bin/octave  

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%  Script to analyze PID control for a spring-mass-damper system
% 
% NOTE: Plotting is set up for output, not viewing on screen.
%       So, it will likely be ugly on screen. The saved PDFs should look
%       better.
%
% Created: 9/17/13 
%   - Joshua Vaughan 
%   - joshua.vaughan@louisiana.edu
%   - http://www.ucs.louisiana.edu/~jev9637
%
% Modified:
%   *
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Utility function to help prettify plotting
%
% Decide if user is using MATLAB or Octave
% This will return a nonzero value if in Octave
isOctave = exist('OCTAVE_VERSION');

if isOctave == 0 % We're in MATLAB
    plot_line_width = 3;
    grid_line_width = 2;
else % We're in Octave
    plot_line_width = 8;
    grid_line_width = 4;
end

% Set consistent font
font_name = 'Times New Roman';



% Simple mass-spring system
%                   +---> X
%                   |
%   /|     k     +-----+
%   /|---/\/\/---|     |
%   /|           |  M  +=====> F
%   /|-----]-----|     |
%   /|     c     +-----+

% Define system parameters
k = 20;             % Spring constant (N/m)
m = 1;              % Mass (kg) 
c = 10;             % damping coefficient 


% Set up the time for simulation; here between 0 and 5s
t = 0:0.01:5;


%----- Start with the open-loop simulation -----------------------------------------------
%
% Define the open-loop system to use in simulation - in transfer function form here
num = [1];
den = [m c k];
sys = tf(num,den);

% Let's start it at t=0.5s for clarity in plotting
F = zeros(1,501);        % Define an array of all zeros
F(1,51:end) = 1;         % Make all elements of this array index>50 = 1 (all after 0.5s)

% run the simulation - utilize the built-in lsim (linear simulation) function
[yout,T,xout] = lsim(sys,F,t);

% Plot the response
%  The plot is formatted for saving, so it might be ugly on screen
h = figure;
set (h,'papertype', '<custom>')
set (h,'paperunits','inches');
set (h,'papersize',[9 6])
set (h,'paperposition', [0,0,[9 6]])
set (gca,'position', [0.16, 0.19, 0.8, 0.75])
set (gca, 'fontsize', 24)

% You can comment out all of the plot prettification and only use this line, if you like
%  It may look better on screen
plot(T,yout,'LineWidth',plot_line_width)
grid on
set (gca, 'LineWidth',grid_line_width)
axis([0 5 0 1.8])

xlabel('Time (s)','fontsize',28)
ylabel('Position (m)','fontsize',28)

FN = findall(h,'-property','FontName');
set(FN,'FontName',font_name);

% check if MATLAB or Octave to descide how to save
if isOctave == 0; % this is MATLAB
    % Save the figure as a high-res pdf
    print(h,'OpenLoop_Step_Resp.pdf','-dpdf');
else
    % Save the figure as a high-res pdf
    print(h,'OpenLoop_Step_Resp.pdf','-dpdf','-color','-landscape')
end





%----- Proporional Control simulation -----------------------------------------------
%
kp = 300;               % Choose the proportional control gain

% Define the closed-loop transfer function
numP = [kp];
denP = [m c (k + kp)];
sysP = tf(numP,denP);

% The input is now the desired position, Xd
% Let's start it at t=0.5s for clarity in plotting
Xd = zeros(1,501);        % Define an array of all zeros
Xd(1,51:end) = 1;         % Make all elements of this array index>50 = 1 (all after 0.5s)

% run the simulation - utilize the built-in lsim (linear simulation) function
[yout_P,T_P,xout_P] = lsim(sysP,Xd,t);

% Plot the response
%  The plot is formatted for saving, so it might be ugly on screen
h = figure;
set (h,'papertype', '<custom>')
set (h,'paperunits','inches');
set (h,'papersize',[9 6])
set (h,'paperposition', [0,0,[9 6]])
set (gca,'position', [0.16, 0.19, 0.8, 0.75])
set (gca, 'fontsize', 24)

% You can comment out all of the plot prettification and only use this line, if you like
%  It may look better on screen
plot(T_P,yout_P,'LineWidth',plot_line_width)
grid on
set (gca, 'LineWidth',grid_line_width)
axis([0 5 0 1.8])

xlabel('Time (s)','fontsize',28)
ylabel('Position (m)','fontsize',28)

FN = findall(h,'-property','FontName');
set(FN,'FontName',font_name);

% check if MATLAB or Octave to descide how to save
if isOctave == 0; % this is MATLAB
    % Save the figure as a high-res pdf
    print(h,'PropControl_Step_Resp_Kp0300.pdf','-dpdf');
else
    % Save the figure as a high-res pdf
    print(h,'PropControl_Step_Resp_Kp0300.pdf','-dpdf','-color','-landscape')
end




%----- Proportional-Derivate Control simulation -----------------------------------------------
%
kp = 300;               % Choose the proportional control gain
kd = 10;                % Choose the derivative control gain

% Define the closed-loop transfer function
numPD = [kd kp];
denPD = [m (c + kd) (k + kp)];
sysPD = tf(numPD,denPD);

% The input is now the desired position, Xd
% Let's start it at t=0.5s for clarity in plotting
Xd = zeros(1,501);        % Define an array of all zeros
Xd(1,51:end) = 1;         % Make all elements of this array index>50 = 1 (all after 0.5s)

% run the simulation - utilize the built-in lsim (linear simulation) function
[yout_PD,T_PD,xout_PD] = lsim(sysPD,Xd,t);

% Plot the response
%  The plot is formatted for saving, so it might be ugly on screen
h = figure;
set (h,'papertype', '<custom>')
set (h,'paperunits','inches');
set (h,'papersize',[9 6])
set (h,'paperposition', [0,0,[9 6]])
set (gca,'position', [0.16, 0.19, 0.8, 0.75])
set (gca, 'fontsize', 24)


% You can comment out all of the plot prettification and only use this line, if you like
%  It may look better on screen
plot(T_PD,yout_PD,'LineWidth',plot_line_width)
grid on
set (gca, 'LineWidth',grid_line_width)
axis([0 5 0 1.8])

xlabel('Time (s)','fontsize',28)
ylabel('Position (m)','fontsize',28)

FN = findall(h,'-property','FontName');
set(FN,'FontName',font_name);

% check if MATLAB or Octave to descide how to save
if isOctave == 0; % this is MATLAB
    % Save the figure as a high-res pdf
    print(h,'PropDerivControl_Step_Resp.pdf','-dpdf');
else
    % Save the figure as a high-res pdf
    print(h,'PropDerivControl_Step_Resp.pdf','-dpdf','-color','-landscape')
end


%----- Proportional-Integral-Derivate Control simulation ---------------------------------
%
kp = 350;               % Choose the proportional control gain
kd = 25;                % Choose the derivative control gain
ki = 300;               % Choose the integral control gain

% Define the closed-loop transfer function
numPID = [kd kp ki];
denPID = [m (c + kd) (k + kp) ki];
sysPID = tf(numPID,denPID);

% The input is now the desired position, Xd
% Let's start it at t=0.5s for clarity in plotting
Xd = zeros(1,501);        % Define an array of all zeros
Xd(1,51:end) = 1;         % Make all elements of this array index>50 = 1 (all after 0.5s)

% run the simulation - utilize the built-in lsim (linear simulation) function
[yout_PID,T_PID,xout_PID] = lsim(sysPID,Xd,t);

% Plot the response
%  The plot is formatted for saving, so it might be ugly on screen
h = figure;
set (h,'papertype', '<custom>')
set (h,'paperunits','inches');
set (h,'papersize',[9 6])
set (h,'paperposition', [0,0,[9 6]])
set (gca,'position', [0.16, 0.19, 0.8, 0.75])
set (gca, 'fontsize', 24)

% You can comment out all of the plot prettification and only use this line, if you like
%  It may look better on screen
plot(T_PID,yout_PID,'LineWidth',plot_line_width)
grid on
set (gca, 'LineWidth',grid_line_width)
axis([0 5 0 1.8])

xlabel('Time (s)','fontsize',28)
ylabel('Position (m)','fontsize',28)

FN = findall(h,'-property','FontName');
set(FN,'FontName',font_name);

% check if MATLAB or Octave to descide how to save
if isOctave == 0; % this is MATLAB
    % Save the figure as a high-res pdf
    print(h,'PropIntDerivControl_Step_Resp.pdf','-dpdf');
else
    % Save the figure as a high-res pdf
    print(h,'PropIntDerivControl_Step_Resp.pdf','-dpdf','-color','-landscape')
end
