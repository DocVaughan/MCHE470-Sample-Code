%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function VideoTracking_Color
% VideoTracking_Color.m
%
% File to analyze video files
%
% Modified from CraneTrack.m developed by Dr. Dave Frakes
%
% Joshua Vaughan (vaughanje@gatech.edu)
%
% modified: 
%  4/30/09 - JEV (vaughanje@gatech.edu)
%       uses "new" mmreader Matlab function
%       this allows formats other than .avi to be read (was .avi only prior)
%       added check for center tracking, allow user to manually input if lost
%
%  1/03/10 - JEV (vaughanje@gatech.edu)
%       Added options for processing white dots on black backgrounds
%  
%  10/25/10 - JEV (vaughanje@gatech.edu)
%       Improved options for choosing type of marker, light or dark
%       Automated movie height and width selection
%
%  7/16/11 - JEV (vaughanje@gatech.edu)
%       Modified tracking algorithm to track a specific color, not just B/W
%       Also uses MATLAB internal image processing, rather than brute force
%
%  8/2/11 - JEV (vaughanje@gatech.edu)
%       Modified to track only top half of video 
%       Added option to plot subplot showing process steps
%
%  9/15/11 - JEV (vaughanje@gatech.edu)
%       "re-generalized" from Cherrypicker processing script
%       Now back to entire video - reversing 8/2/11 change
%
% 10/21/11 - JEV (vaughanje@gatech.edu)
%       Allow user to draw around color to track
%       Track in LAB space, not RGB
%
% 11/1/11 - JEV (vaughanje@gatech.edu)
%       Code cleanup
%       Added option to exclude movie data from filesave - results in much
%           smaller file sizes
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
clear all
fontSize = 10;

% Ask user for video file to process
[File,Dir] = uigetfile('*.*','Select your file');
file_location = strcat(Dir,File);

movie1 = mmreader(file_location);       % video title

q1 = 1;                                 % start frame number
q2 = get(movie1, 'numberOfFrames');     % end frame nubmer

% Read in video frames.
vidFrames = read(movie1,[q1 q2]);

% get video properties
fps = movie1.FrameRate;
deltaT = 1/fps;
height = movie1.height;
width = movie1.width;

% define to speed computation
data = zeros(1,2,q2-q1+1);
im0 = vidFrames(:,:,:,1);
rgbImage = im0;
[rows columns numberOfColorBands] = size(rgbImage); 

% Display the original image.
	h1 = subplot(2, 2, 1);
	imshow(rgbImage);
	drawnow; % Make it display immediately. 
	if numberOfColorBands > 1 
		title('Original Color Image', 'FontSize', fontSize); 
	else 
		caption = sprintf('Original Indexed Image\n(converted to true color with its stored colormap)');
		title(caption, 'FontSize', fontSize);
	end
	
	% Let user outline region over rgb image.
	mask = DrawFreehandRegion(h1, rgbImage);  % Draw a freehand, irregularly-shaped region.
	
    subplot(2, 2, 1);
	imshow(rgbImage);
    if numberOfColorBands > 1 
		title('Original Color Image', 'FontSize', fontSize); 
	else 
		caption = sprintf('Original Indexed Image\n(converted to true color with its stored colormap)');
		title(caption, 'FontSize', fontSize);
	end
    
% 	% Mask the image.
% 	maskedRgbImage = bsxfun(@times, rgbImage, cast(mask, class(rgbImage)));
% 	% Display it.
% 	subplot(3, 4, 5);
% 	imshow(maskedRgbImage);
% 	title('The Region You Drew', 'FontSize', fontSize); 

	% Convert image from RGB colorspace to lab color space.
	cform = makecform('srgb2lab');
	lab_Image = applycform(im2double(rgbImage),cform);
	
	% Extract out the color bands from the original image
	% into 3 separate 2D arrays, one for each color component.
	LChannel = lab_Image(:, :, 1); 
	aChannel = lab_Image(:, :, 2); 
	bChannel = lab_Image(:, :, 3); 
	
% 	% Uncomment sectio below to Display the lab images.
%   figure
% 	subplot(1, 3, 1);
% 	imshow(LChannel, []);
% 	title('L Channel', 'FontSize', fontSize);
% 	subplot(1, 3, 2);
% 	imshow(aChannel, []);
% 	title('a Channel', 'FontSize', fontSize);
% 	subplot(1, 3, 3);
% 	imshow(bChannel, []);
% 	title('b Channel', 'FontSize', fontSize);

	% Get the average lab color value.
	[LMean, aMean, bMean] = GetMeanLABValues(LChannel, aChannel, bChannel, mask);
	
	% Make uniform images of only that one single LAB color.
	LStandard = LMean * ones(rows, columns);
	aStandard = aMean * ones(rows, columns);
	bStandard = bMean * ones(rows, columns);
	
	% Create the delta images: delta L, delta A, and delta B.
	deltaL = LChannel - LStandard;
	deltaa = aChannel - aStandard;
	deltab = bChannel - bStandard;
	
	% Create the Delta E image.
	% This is an image that represents the color difference.
	% Delta E is the square root of the sum of the squares of the delta images.
	deltaE = sqrt(deltaL .^ 2 + deltaa .^ 2 + deltab .^ 2);
	
	% Mask it to get the Delta E in the mask region only.
	maskedDeltaE = deltaE .* mask;
	% Get the mean delta E in the mask region
	% Note: deltaE(mask) is a 1D vector of ONLY the pixel values within the masked area.
 	meanMaskedDeltaE = mean(deltaE(mask));
	% Get the standard deviation of the delta E in the mask region
	stDevMaskedDeltaE = std(deltaE(mask));
	message = sprintf('The mean LAB = (%.2f, %.2f, %.2f).\nThe mean Delta E in the masked region is %.2f +/- %.2f',...
		LMean, aMean, bMean, meanMaskedDeltaE, stDevMaskedDeltaE);	
	
% 	% Display the masked Delta E image - the delta E within the masked region only.
% 	subplot(3, 4, 6);
% 	imshow(maskedDeltaE, []);
% 	caption = sprintf('Delta E between image within masked region\nand mean color within masked region.\n(With amplified intensity)');
% 	title(caption, 'FontSize', fontSize);

	% Display the Delta E image - the delta E over the entire image.
	subplot(2, 2, 2);
	imshow(deltaE, []);
	caption = sprintf('Delta E Image\n(Darker = Better Match)');
	title(caption, 'FontSize', fontSize);

    % Plot the histograms of the Delta E color difference image,
	% both within the masked region, and for the entire image.
	PlotHistogram(deltaE(mask), deltaE, [2 2 3], 'Histograms of the 2 Delta E Images');

    
	% Find out how close the user wants to match the colors.
	prompt = {sprintf('First, examine the histogram.\nThen find pixels within this Delta E (from the average color in the region you drew):')};
	dialogTitle = 'Enter Delta E Tolerance';
	numberOfLines = 1;
	% Set the default tolerance to be the mean delta E in the masked region plus two standard deviations.
	strTolerance = sprintf('%.1f', meanMaskedDeltaE + 3 * stDevMaskedDeltaE);
	defaultAnswer = {strTolerance};  % Suggest this number to the user.
	response = inputdlg(prompt, dialogTitle, numberOfLines, defaultAnswer);
	% Update tolerance with user's response.
	tolerance = str2double(cell2mat(response));

	
	% Place a vertical bar at the threshold location.
	handleToSubPlot8 = subplot(2, 2, 3);  % Get the handle to the plot.
	PlaceVerticalBarOnPlot(handleToSubPlot8, tolerance, [0 .5 0]);  % Put a vertical red line there.
    
    % Find pixels within that delta E.
	binaryImage = deltaE <= tolerance;
	subplot(2, 2, 4);
	imshow(binaryImage, []);
	title('Matching Colors Mask', 'FontSize', fontSize);
	

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Size of sub-area to track, in pixels
% Adjust according to image and object size
d2=200;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

figure;
imshow(binaryImage);

cent=zeros(1,2);
for n1=1,
    [cent(n1,1) cent(n1,2)]=ginput(1);
end;
cent=round(cent);   
newvect=round(cent);
    
    
% if =1, display each frame & create video showing angles
plot_flag = 0;  

% if =1, display subplot showing image processing steps
sub_plot_flag = 0;  

% counter variable
count = 1;

% Loop through frames from q1 to q2
for n = q1:q2
    
    % Get current frame, n - this is the full frame
    data_full = vidFrames(:,:,:,n-q1+1);
    data = data_full;
    
    newvect=round(cent);

    if sub_plot_flag == 1
        Process_Figure = figure
        subplot(2,3,1)
        imshow(data)
        title('Frame Before Any Processing')
    end
    
    % Convert image from RGB colorspace to LAB color space.
	cform = makecform('srgb2lab');
	lab_Image = applycform(im2double(data),cform);
    

	% Extract out the color bands from the original image
	% into 3 separate 2D arrays, one for each color component.
	LChannel = lab_Image(:, :, 1); 
	aChannel = lab_Image(:, :, 2); 
	bChannel = lab_Image(:, :, 3); 
	
	% Create the delta images: delta L, delta A, and delta B.
	deltaL = LChannel - LStandard;
	deltaa = aChannel - aStandard;
	deltab = bChannel - bStandard;
	
	% Create the Delta E image.
	% This is an image that represents the color difference.
	% Delta E is the square root of the sum of the squares of the delta images.
	deltaE = sqrt(deltaL .^ 2 + deltaa .^ 2 + deltab .^ 2);
    
    diff_im = deltaE <= tolerance;
      
    if sub_plot_flag == 1
        figure(Process_Figure)
        subplot(2,3,2)
        imshow(diff_im,[]);
        title('Matching Colors Mask');
    end
    
    
    %Use a median filter to filter out noise
    %     B = MEDFILT2(A,[M N]) performs median filtering of the matrix
    %     A in two dimensions. Each output pixel contains the median
    %     value in the M-by-N neighborhood around the corresponding
    %     pixel in the input image. MEDFILT2 pads the image with zeros
    %     on the edges, so the median values for the points within 
    %     [M N]/2 of the edges may appear distorted.
    diff_im = medfilt2(diff_im, [3 3]);
    if sub_plot_flag == 1
        figure(Process_Figure)
        subplot(2,3,3)
        imshow(diff_im);
        title('After Median Filter')
    end
    
    
    % Remove all those pixels less than 200px area
    %     BW2 = BWAREAOPEN(BW,P) removes from a binary image all connected
    %     components (objects) that have fewer than P pixels, producing another
    %     binary image BW2. 
    diff_im = bwareaopen(diff_im,100);
    if sub_plot_flag == 1;
        figure(Process_Figure)
        subplot(2,3,4)
        imshow(diff_im);
        title('After Eliminating Small Objects');
    end
    
    % Set up edge-finding/outline parameters
    se90 = strel('line', 3, 90);
    se0 = strel('line', 3, 0);
    
    % Define outlines around detected object "blobs"
    %  Here, imdilate looks for straight lines 3 pixels long
    diff_im = imdilate(diff_im, [se90 se0]);
    
    % fill in interior holes
    %     BW2 = IMFILL(BW1,'holes') fills holes in the input image.  A hole is
    %     a set of background pixels that cannot be reached by filling in the
    %     background from the edge of the image.
    diff_im = imfill(diff_im, 'holes');
    if sub_plot_flag == 1
        figure(Process_Figure)
        subplot(2,3,5)
        imshow(diff_im);
        title('Binary Image with Filled Holes');
    end
%     
    seD = strel('diamond',1);
    diff_im = imerode(diff_im,seD);
    
%     Limit inspection box - just make all outside box black
[xpix,ypix] = size(diff_im);
for ii = 1:xpix
    for jj = 1:ypix
        
        if (ii > cent(2)-d2/2 && jj > cent(1)-d2/2) && (ii < cent(2)+d2/2 && jj < cent(1)+d2/2)
            final_im(ii,jj) = diff_im(ii,jj);
        else
            final_im(ii,jj) = 0;
        end
    end
end;

    if sub_plot_flag == 1
        figure(Process_Figure)
        subplot(2,3,6)
        imshow(final_im), 
        title('After All Frame Cleanup');
    end
    

% Identify and label the blobs in the current frame.
bw = bwlabel(final_im, 8);


% Image blob analysis.
% We get a set of properties for each labeled blob.
stats = regionprops(bw, 'Centroid','ConvexHull','Orientation');
numberOfBlobs = size(stats, 1);

if numberOfBlobs == 0
    disp('Centroid was lost.  Click on point to track.')
    figure
    imshow(diff_im);
    [cent(1,1) cent(1,2)]=ginput(1);
    cent=round(cent);
    center(1,:,n) = cent;
else
    
    if plot_flag == 1
        figure
        % Display the image
        imshow(data_full)
        hold on % hold plot in order to overlay information
    end
    
    
    
    % This is a loop to bound the color objects in the detected convex hull
    % Creates an image containing key properties identified
    for object = 1:numberOfBlobs
        bc = stats(object).Centroid;
        bh = stats(object).ConvexHull;
        bo = stats(object).Orientation; % Approximate each blob as an ellipse
        
        
        if plot_flag == 1
            plot(bc(1),bc(2),'bo','MarkerSize',10,'MarkerFaceColor','b')    % Plot centeroid
            plot(bh(:,1),bh(:,2),'r')   % Plot convex hull
            
            % Add object number text
            text(bc(1), bc(2)-15, num2str(object), 'FontSize', 12, 'FontWeight', 'Bold');
            
            % Add angle text
            a=text(bc(1)-20,bc(2), strcat('Angle: ',num2str(round(bo))));
            
            % Set font properties for angle text
            set(a, 'FontName', 'Arial', 'FontWeight', 'bold', 'FontSize', 12, 'Color', 'black');
            pause
        end
        
        % Record ojbect properties
        center(object,:,n) = bc;
        angle(object,:,n) = bo;
    end
    
    cent = center(1,:,n);
    
end

offset=cent-newvect;
cent=cent+offset;
    
    if plot_flag == 1
       hold off
       
       % Save frame for movie
       M(count) = getframe(gcf); 
       
       % Close image of current frame
        close all;
    end
    
    
    % Uncomment below to print frame number and object center to command window
    %   during processing
    % Useful for tracking progress of the code
    str = sprintf('Frame Number: %d \t--\t Center: (%d,%d)',count,round(cent(1)),round(cent(2)));
    disp(str)
    
    count = count+1;
    
end


% Extract key points for analysis - raw data, all blobs
time = 0:deltaT:(q2-1)*deltaT;

% xpixel and ypixel data
x_pixel = squeeze(center(1,1,:));
y_pixel = squeeze(center(1,2,:));

% Include movie data with file save?
button = questdlg(sprintf('Include movie data with filesave? \nDoing so will result in large file sizes.'),'Include Movie Data?','Do Not Include','Include Movie Data','Do Not Include'); 
if button == 'Do Not Include'
   clear vidFrames
end
        
% save data as .mat file
% [file,path] = uiputfile('*.mat','Save Data As');
uisave

return;



%-----------------------------------------------------------------------------
function [xCoords, yCoords, roiPosition] = DrawBoxRegion(handleToImage)
	try
	% Open a temporary full-screen figure if requested.
	enlargeForDrawing = true;
	axes(handleToImage);
	if enlargeForDrawing
		hImage = findobj(gca,'Type','image');
		numberOfImagesInside = length(hImage);
		if numberOfImagesInside > 1
			imageInside = get(hImage(1), 'CData');
		else
			imageInside = get(hImage, 'CData');
		end
		hTemp = figure;
		hImage2 = imshow(imageInside, []);
		[rows columns NumberOfColorBands] = size(imageInside);
		set(gcf, 'Position', get(0,'Screensize')); % Maximize figure.
	end
	
	txtInfo = sprintf('Draw a box over the unstained fabric by clicking and dragging over the image.\nDouble click inside the box to finish drawing.');
	text(10, 40, txtInfo, 'color', 'r', 'FontSize', 24);

    % Prompt user to draw a region on the image.
	msgboxw(txtInfo);
	
	% Erase all previous lines.
	if ~enlargeForDrawing
		axes(handleToImage);
% 		ClearLinesFromAxes(handles);
	end
	
	hBox = imrect;
	roiPosition = wait(hBox);
	roiPosition
	% Erase all previous lines.
	if ~enlargeForDrawing
		axes(handleToImage);
% 		ClearLinesFromAxes(handles);
	end

	xCoords = [roiPosition(1), roiPosition(1)+roiPosition(3), roiPosition(1)+roiPosition(3), roiPosition(1), roiPosition(1)];
	yCoords = [roiPosition(2), roiPosition(2), roiPosition(2)+roiPosition(4), roiPosition(2)+roiPosition(4), roiPosition(2)];

	% Plot the mask as an outline over the image.
	hold on;
	plot(xCoords, yCoords, 'linewidth', 2);
	close(hTemp);
	catch ME
		errorMessage = sprintf('Error running DrawRegion:\n\n\nThe error message is:\n%s', ...
			ME.message);
		WarnUser(errorMessage);
	end
	return; % from DrawRegion
	
%-----------------------------------------------------------------------------
function [mask] = DrawFreehandRegion(handleToImage, rgbImage)
try
	fontSize = 14;
	% Open a temporary full-screen figure if requested.
	enlargeForDrawing = true;
	axes(handleToImage);
	if enlargeForDrawing
		hImage = findobj(gca,'Type','image');
		numberOfImagesInside = length(hImage);
		if numberOfImagesInside > 1
			imageInside = get(hImage(1), 'CData');
		else
			imageInside = get(hImage, 'CData');
		end
		hTemp = figure;
		hImage2 = imshow(imageInside, []);
		[rows columns NumberOfColorBands] = size(imageInside);
		set(gcf, 'Position', get(0,'Screensize')); % Maximize figure.
	end
	
	message = sprintf('Left click and hold to begin drawing.\nSimply lift the mouse button to finish');
	text(10, 40, message, 'color', 'r', 'FontSize', fontSize);

    % Prompt user to draw a region on the image.
	uiwait(msgbox(message));
	
	% Now, finally, have the user freehand draw the mask in the image.
	hFH = imfreehand();

	% Once we get here, the user has finished drawing the region.
	% Create a binary image ("mask") from the ROI object.
	mask = hFH.createMask();
	
	% Close the maximized figure because we're done with it.
	close(hTemp);

	% Display the freehand mask.
	subplot(3, 4, 5);
	imshow(mask);
	title('Binary mask of the region', 'FontSize', fontSize);
	
	% Mask the image.
	maskedRgbImage = bsxfun(@times, rgbImage, cast(mask,class(rgbImage)));
	% Display it.
	subplot(3, 4, 6);
	imshow(maskedRgbImage);
catch ME
	errorMessage = sprintf('Error running DrawFreehandRegion:\n\n\nThe error message is:\n%s', ...
		ME.message);
	WarnUser(errorMessage);
end
return; % from DrawFreehandRegion

%-----------------------------------------------------------------------------
% Get the average lab within the mask region.
function [LMean, aMean, bMean] = GetMeanLABValues(LChannel, aChannel, bChannel, mask)
try
	LVector = LChannel(mask); % 1D vector of only the pixels within the masked area.
	LMean = mean(LVector);
	aVector = aChannel(mask); % 1D vector of only the pixels within the masked area.
	aMean = mean(aVector);
	bVector = bChannel(mask); % 1D vector of only the pixels within the masked area.
	bMean = mean(bVector);
catch ME
	errorMessage = sprintf('Error running GetMeanLABValues:\n\n\nThe error message is:\n%s', ...
		ME.message);
	WarnUser(errorMessage);
end
return; % from GetMeanLABValues

%==========================================================================================================================
% Plots the histograms of the pixels in both the masked region and the entire image.
function PlotHistogram(maskedRegion, doubleImage, plotNumber, caption)
try
	fontSize = 14;
	subplot(plotNumber(1), plotNumber(2), plotNumber(3)); 

	% Find out where the edges of the histogram bins should be.
	maxValue1 = max(maskedRegion(:));
	maxValue2 = max(doubleImage(:));
	maxOverallValue = max([maxValue1 maxValue2]);
	edges = linspace(0, maxOverallValue, 100);

	% Get the histogram of the masked region into 100 bins.
	pixelCount1 = histc(maskedRegion(:), edges);

	% Get the histogram of the entire image into 100 bins.
	pixelCount2 = histc(doubleImage(:), edges);

	% Plot the  histogram of the entire image.
	plot(edges, pixelCount2, 'b-');
	
	% Now plot the histogram of the masked region.
	% However there will likely be so few pixels that this plot will be so low and flat compared to the histogram of the entire
	% image that you probably won't be able to see it.  To get around this, let's scale it to make it higher so we can see it.
	gainFactor = 1.0;
	maxValue3 = max(max(pixelCount2));
	pixelCount3 = gainFactor * maxValue3 * pixelCount1 / max(pixelCount1);
	hold on;
	plot(edges, pixelCount3, 'r-');
	title(caption, 'FontSize', fontSize);
	
	% Scale x axis manually.
	xlim([0 edges(end)]);
	legend('Entire', 'Masked');
	
catch ME
	errorMessage = sprintf('Error running PlotHistogram:\n\n\nThe error message is:\n%s', ...
		ME.message);
	WarnUser(errorMessage);
end
return; % from PlotHistogram

%==========================================================================================================================
function WarnUser(warningMessage)
	uiwait(warndlg(warningMessage));
	return; % from WarnUser()
	
%==========================================================================================================================
function msgboxw(message)
	uiwait(msgbox(message));
	return; % from msgboxw()
    
    %=====================================================================
% Shows vertical lines going up from the X axis to the curve on the plot.
function lineHandle = PlaceVerticalBarOnPlot(handleToPlot, x, lineColor)
	try
		% If the plot is visible, plot the line.
		if get(handleToPlot, 'visible')
			axes(handleToPlot);  % makes existing axes handles.axesPlot the current axes.
			% Make sure x location is in the valid range along the horizontal X axis.
			XRange = get(handleToPlot, 'XLim');
			maxXValue = XRange(2);
			if x > maxXValue
				x = maxXValue;
			end
			% Erase the old line.
			%hOldBar=findobj('type', 'hggroup');
			%delete(hOldBar);
			% Draw a vertical line at the X location.
			hold on;
			yLimits = ylim;
			lineHandle = line([x x], [yLimits(1) yLimits(2)], 'Color', lineColor, 'LineWidth', 3);
			hold off;
		end
	catch ME
		errorMessage = sprintf('Error running PlaceVerticalBarOnPlot:\n\n\nThe error message is:\n%s', ...
			ME.message);
		WarnUser(errorMessage);
end
	return;	% End of PlaceVerticalBarOnPlot

