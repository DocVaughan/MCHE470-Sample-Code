% this line allows running directly from the shell... probably leaved commented out
% #!/usr/local/bin/octave  

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%  Script to analyze processing for a noisy, constant voltage signale
% 
% NOTE: Plotting is set up for output, not viewing on screen.
%       So, it will likely be ugly on screen. The saved PDFs should look
%       better.
%
% Created: 10/21/13 
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



% Set up the time for simulation; here between 0 and 5s
deltaT = 0.01;
t = 0:deltaT:5;

act_volt = [0.75*ones(1,251) 1.5*ones(1,250)];

noise = 0.25*randn(1,length(t));

measured_volt = act_volt + noise;


%---- Plot the "raw" data along with the actual voltage ----------------------------------
%  The plot is formatted for saving, so it might be ugly on screen
h = figure;

% Define the papersize and margins
set (h,'papertype', '<custom>')
set (h,'paperunits','inches');

% papersize is 9" x 6" - 3x2 aspect ratio is best
set (h,'papersize',[9 6])       
set (h,'paperposition', [0,0,[9 6]])

% set the margins as percentage of page
set (gca,'position', [0.19, 0.19, 0.75, 0.75]) 

% Increase the axis font size to somethign readable
set (gca, 'fontsize', 24)

% The options are only specified once in MATLAB. Octave let's you adjust
% each line. This means we need to define the LineWidth for each variable
% in Octave.
if isOctave == 0 % We're in MATLAB
    plot(t,measured_volt,t,act_volt,'--','LineWidth',plot_line_width)
else % We're in Octave 
    plot(t,measured_volt,'--','LineWidth',plot_line_width,t,act_volt,'r','LineWidth',plot_line_width)
end

% Show a grid and set an appropriate line thickness 
grid on
set (gca, 'LineWidth',grid_line_width)

% Set the X and Y axis labels - Change these to suit your plot
xlabel('Time (s)','fontsize',28)
ylabel('Voltage (V)','fontsize',28)

axis([0 5 0.0 3.0])

% Create the legend - change 'Data i' to suit your plot
leg = legend('Measured Voltage','Actual Voltage');
set (leg, 'FontSize', 20,'FontName',font_name) 

% Change all fonts to font_name
FN = findall(h,'-property','FontName');
set(FN,'FontName',font_name);


% check if MATLAB or Octave to descide how to save
if isOctave == 0; % this is MATLAB
    % Save the figure as a high-res pdf
    print(h,'Actual_v_Measured_Voltage.pdf','-dpdf');
else
    % Save the figure as a high-res pdf
    print(h,'Actual_v_Measured_Voltage.pdf','-dpdf','-color','-landscape')
end



%----- Let's try some simple filtering ---------------------------------------------------
%
%----- Look at a running average -----

sn = 0;
running_ave(1) = 0;

for ii = 1:length(measured_volt)-1
    sn = sn + measured_volt(ii);
    running_ave(ii+1) = 1/(ii+1)*(sn + measured_volt(ii+1));
end


%---- Compare to actual and measured  voltages ----------------------------------
%  The plot is formatted for saving, so it might be ugly on screen
h = figure;

% Define the papersize and margins
set (h,'papertype', '<custom>')
set (h,'paperunits','inches');

% papersize is 9" x 6" - 3x2 aspect ratio is best
set (h,'papersize',[9 6])       
set (h,'paperposition', [0,0,[9 6]])

% set the margins as percentage of page
set (gca,'position', [0.19, 0.19, 0.75, 0.75]) 

% Increase the axis font size to somethign readable
set (gca, 'fontsize', 24)

% The options are only specified once in MATLAB. Octave let's you adjust
% each line. This means we need to define the LineWidth for each variable
% in Octave.
if isOctave == 0 % We're in MATLAB
    plot(t,measured_volt,'--',t,running_ave,'r','LineWidth',plot_line_width)
else % We're in Octave 
    plot(t,measured_volt,'--','LineWidth',plot_line_width,t,running_ave,'r','LineWidth',plot_line_width)
end

% Show a grid and set an appropriate line thickness 
grid on
set (gca, 'LineWidth',grid_line_width)

% Set the X and Y axis labels - Change these to suit your plot
xlabel('Time (s)','fontsize',28)
ylabel('Voltage (V)','fontsize',28)

axis([0 5 0.0 3.0])

% Create the legend - change 'Data i' to suit your plot
leg = legend('Measured Voltage','Running Average');
set (leg, 'FontSize', 20,'FontName',font_name) 

% Change all fonts to font_name
FN = findall(h,'-property','FontName');
set(FN,'FontName',font_name);


filename = sprintf('Running_Ave.pdf');
% check if MATLAB or Octave to descide how to save
if isOctave == 0; % this is MATLAB
    % Save the figure as a high-res pdf
    print(h,filename,'-dpdf');
else
    % Save the figure as a high-res pdf
    print(h,filename,'-dpdf','-color','-landscape')
end




%----- Look at a moving average -----
num_ave = 25;            % number of points to average
moving_ave = filter(ones(num_ave,1)/num_ave,1,measured_volt);

%---- Compare to actual and measured  voltages ----------------------------------
%  The plot is formatted for saving, so it might be ugly on screen
h = figure;

% Define the papersize and margins
set (h,'papertype', '<custom>')
set (h,'paperunits','inches');

% papersize is 9" x 6" - 3x2 aspect ratio is best
set (h,'papersize',[9 6])       
set (h,'paperposition', [0,0,[9 6]])

% set the margins as percentage of page
set (gca,'position', [0.19, 0.19, 0.75, 0.75]) 

% Increase the axis font size to somethign readable
set (gca, 'fontsize', 24)

% The options are only specified once in MATLAB. Octave let's you adjust
% each line. This means we need to define the LineWidth for each variable
% in Octave.
if isOctave == 0 % We're in MATLAB
    plot(t,measured_volt,'--',t,moving_ave,'r','LineWidth',plot_line_width)
else % We're in Octave 
    plot(t,measured_volt,'--','LineWidth',plot_line_width,t,moving_ave,'r','LineWidth',plot_line_width)
end

% Show a grid and set an appropriate line thickness 
grid on
set (gca, 'LineWidth',grid_line_width)

% Set the X and Y axis labels - Change these to suit your plot
xlabel('Time (s)','fontsize',28)
ylabel('Voltage (V)','fontsize',28)

axis([0 5 0.0 3.0])

% Create the legend - change 'Data i' to suit your plot
ave_legend = sprintf('%d-point Moving Average',num_ave);
leg = legend('Measured Voltage',ave_legend);
set (leg, 'FontSize', 20,'FontName',font_name) 

% Change all fonts to font_name
FN = findall(h,'-property','FontName');
set(FN,'FontName',font_name);


filename = sprintf('%dPoint_MovingAve.pdf',num_ave);
% check if MATLAB or Octave to descide how to save
if isOctave == 0; % this is MATLAB
    % Save the figure as a high-res pdf
    print(h,filename,'-dpdf');
else
    % Save the figure as a high-res pdf
    print(h,filename,'-dpdf','-color','-landscape')
end



%----- Look at low pass filter -----
a = deltaT/0.25;
lowpass_filtered = filter(a,[1 a-1],measured_volt); 

% save for plotting the filter characteristics
lowpass = tf(a,[1 a-1],deltaT);
[mag,phase,freq] = bode(lowpass);
mag = 20*log10(mag);        % convert magnitude to dB

%---- Compare to actual and measured  voltages ----------------------------------
%  The plot is formatted for saving, so it might be ugly on screen
h = figure;

% Define the papersize and margins
set (h,'papertype', '<custom>')
set (h,'paperunits','inches');

% papersize is 9" x 6" - 3x2 aspect ratio is best
set (h,'papersize',[9 6])       
set (h,'paperposition', [0,0,[9 6]])

% set the margins as percentage of page
set (gca,'position', [0.19, 0.19, 0.75, 0.75]) 

% Increase the axis font size to somethign readable
set (gca, 'fontsize', 24)

% The options are only specified once in MATLAB. Octave let's you adjust
% each line. This means we need to define the LineWidth for each variable
% in Octave.
if isOctave == 0 % We're in MATLAB
    plot(t,measured_volt,'--',t,lowpass_filtered,'r','LineWidth',plot_line_width)
else % We're in Octave 
    plot(t,measured_volt,'--','LineWidth',plot_line_width,t,lowpass_filtered,'r','LineWidth',plot_line_width)
end

% Show a grid and set an appropriate line thickness 
grid on
set (gca, 'LineWidth',grid_line_width)

% Set the X and Y axis labels - Change these to suit your plot
xlabel('Time (s)','fontsize',28)
ylabel('Voltage (V)','fontsize',28)

axis([0 5 0.0 3.0])

% Create the legend - change 'Data i' to suit your plot
leg = legend('Measured Voltage','Low Pass Filtered');
set (leg, 'FontSize', 20,'FontName',font_name) 

% Change all fonts to font_name
FN = findall(h,'-property','FontName');
set(FN,'FontName',font_name);


filename = sprintf('LowPass_Filtered.pdf');
% check if MATLAB or Octave to descide how to save
if isOctave == 0; % this is MATLAB
    % Save the figure as a high-res pdf
    print(h,filename,'-dpdf');
else
    % Save the figure as a high-res pdf
    print(h,filename,'-dpdf','-color','-landscape')
end


% plot the filter freq-resp.
%---- Compare to actual and measured  voltages ----------------------------------
%  The plot is formatted for saving, so it might be ugly on screen
h = figure;

% Define the papersize and margins
set (h,'papertype', '<custom>')
set (h,'paperunits','inches');

% papersize is 9" x 6" - 3x2 aspect ratio is best
set (h,'papersize',[9 6])       
set (h,'paperposition', [0,0,[9 6]])

% set the margins as percentage of page
set (gca,'position', [0.19, 0.19, 0.75, 0.75]) 

% Increase the axis font size to somethign readable
set (gca, 'fontsize', 24)

% The options are only specified once in MATLAB. Octave let's you adjust
% each line. This means we need to define the LineWidth for each variable
% in Octave.
if isOctave == 0 % We're in MATLAB
    semilogx(freq,mag,'LineWidth',plot_line_width)
else % We're in Octave 
    semilogx(freq,mag,'LineWidth',plot_line_width)
end

% Show a grid and set an appropriate line thickness 
grid on
set (gca, 'LineWidth',grid_line_width)

% Set the X and Y axis labels - Change these to suit your plot
xlabel('Frequency (rad/s)','fontsize',28)
ylabel('Magnitude (dB)','fontsize',28)

axis([min(freq) 300 1.25*min(mag) 5])

% Create the legend - change 'Data i' to suit your plot
% leg = legend('Measured Voltage','Low Pass Filtered');
% set (leg, 'FontSize', 20,'FontName',font_name) 

% Change all fonts to font_name
FN = findall(h,'-property','FontName');
set(FN,'FontName',font_name);


filename = sprintf('LowPass_FreqResp.pdf');
% check if MATLAB or Octave to descide how to save
if isOctave == 0; % this is MATLAB
    % Save the figure as a high-res pdf
    print(h,filename,'-dpdf');
else
    % Save the figure as a high-res pdf
    print(h,filename,'-dpdf','-color','-landscape')
end





% ----- Now let's look at a Kalman Filter ------------------------------------------------
A = 1;          % state transition matrix
B = 1;          % control-input matrix (no input here, so =0)

H = 1;          % observation matrix (Estimating voltage and are measuring volts so = 1)

Q = 0.001;      % process covariance 

R = 0.5;        % measurement covariance (how noisy is the measurement?)

volt_init = 1;    % initial guess of the system state

input = act_volt;

% create empty matrices to fill during solution
volt = zeros(1,length(measured_volt)); 
P = zeros(1,length(measured_volt));

% fill the first value with the initial guess
volt(1) = volt_init;  % initial state estimate is the initial guess
P(1) = 1;       % prediction covariance (1 because we don't know better)

% input = 0;                  % no input

for ii = 2:length(measured_volt)
    % Prediction step - current estimates using model
    volt_pred = A*volt(ii-1) + B*input(ii);
    P_pred = A*P(ii-1)*A' + Q;

    % Observation step
    volt_bar = measured_volt(ii) - H*volt_pred;
    S = H*P_pred*H' + R;
    K = P_pred*H'*inv(S);
    volt_est(ii) = volt_pred + K*volt_bar;
    P(ii) = (1 - K*H)*P_pred;
end

%---- Compare to actual and measured  voltages ----------------------------------
%  The plot is formatted for saving, so it might be ugly on screen
h = figure;

% Define the papersize and margins
set (h,'papertype', '<custom>')
set (h,'paperunits','inches');

% papersize is 9" x 6" - 3x2 aspect ratio is best
set (h,'papersize',[9 6])       
set (h,'paperposition', [0,0,[9 6]])

% set the margins as percentage of page
set (gca,'position', [0.19, 0.19, 0.75, 0.75]) 

% Increase the axis font size to somethign readable
set (gca, 'fontsize', 24)

% The options are only specified once in MATLAB. Octave let's you adjust
% each line. This means we need to define the LineWidth for each variable
% in Octave.
if isOctave == 0 % We're in MATLAB
    plot(t,measured_volt,'--',t,volt_est,'r','LineWidth',plot_line_width)
else % We're in Octave 
    plot(t,measured_volt,'--','LineWidth',plot_line_width,t,volt_est,'r','LineWidth',plot_line_width)
end

% Show a grid and set an appropriate line thickness 
grid on
set (gca, 'LineWidth',grid_line_width)

% Set the X and Y axis labels - Change these to suit your plot
xlabel('Time (s)','fontsize',28)
ylabel('Voltage (V)','fontsize',28)

axis([0 5 0.0 3.0])

% Create the legend - change 'Data i' to suit your plot
leg = legend('Measured Voltage','Kalman Filtered');
set (leg, 'FontSize', 20,'FontName',font_name) 

% Change all fonts to font_name
FN = findall(h,'-property','FontName');
set(FN,'FontName',font_name);


filename = sprintf('Kalman_Filtered.pdf');
% check if MATLAB or Octave to descide how to save
if isOctave == 0; % this is MATLAB
    % Save the figure as a high-res pdf
    print(h,filename,'-dpdf');
else
    % Save the figure as a high-res pdf
    print(h,filename,'-dpdf','-color','-landscape')
end

