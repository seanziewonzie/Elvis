function varargout = leastTime(varargin)

%
% Author: 
%   Zachary Bradshaw
%
% Usage: 
%   leastTime  - function that creates gui & components
%   varargout - represents any number of output arguments
%   varargin  - represents any number of input arguments
% 
% [fig] - add initial figure
fig = figure(...
    'Tag',             'fig',...
    'Name',            'Least Time Interface',...
    'NumberTitle',     'off',...
    'Visible',         'on',... 
    'MenuBar',         'none',...
    'Units',           'normalized',...
    'UserData',        struct(... % use for passing params
                            'plotData',[],...
                            'resultData',[]...
                       ),...
    'Position',        [.1 .1 .75 .75]);



%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Add Toolbar & Push Buttons                                   %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% add toolbar
tb = uitoolbar('Parent',fig);

% get open icon png & convert to use in toolbar
[img_open,~,alpha] = imread(fullfile(matlabroot,...
    'toolbox/matlab/icons/file_open.png'));
openIcon = double(img_open)/256/256;
openIcon(~alpha) = NaN;

% get save icon png & convert to use in toolbar
[img_save,~,alpha] = imread(fullfile(matlabroot,...
    'toolbox/matlab/icons/file_save.png'));
saveIcon = double(img_save)/256/256;
saveIcon(~alpha) = NaN;

% get pan icon png & convert to use in toolbar
[img_save,~,alpha] = imread(fullfile(matlabroot,...
    'toolbox/matlab/icons/tool_hand.png'));
panIcon = double(img_save)/256/256;
panIcon(~alpha) = NaN;

% get zoom in icon png & convert to use in toolbar
[img_save,~,alpha] = imread(fullfile(matlabroot,...
    'toolbox/matlab/icons/tool_zoom_in.png'));
zoomInIcon = double(img_save)/256/256;
zoomInIcon(~alpha) = NaN;

% get zoom in icon png & convert to use in toolbar
[img_save,~,alpha] = imread(fullfile(matlabroot,...
    'toolbox/matlab/icons/tool_zoom_out.png'));
zoomOutIcon = double(img_save)/256/256;
zoomOutIcon(~alpha) = NaN;

% [openBtn] - open button
uipushtool(...
    'Parent',          tb,...
    'Tag',             'openBtn',...
    'CData',           openIcon,...
    'TooltipString',   'Open File',...
    'ClickedCallback', @openBtnCallback);

% [saveBtn] - save button
uipushtool(...
    'Parent',          tb,...
    'Tag',             'saveBtn',...
    'CData',           saveIcon,...
    'TooltipString',   'Save File',...
    'ClickedCallback', @saveBtnCallback);

% [panBtn] - pan button
uipushtool(...
    'Parent',          tb,...
    'Tag',             'panBtn',...
    'CData',           panIcon,...
    'TooltipString',   'pan tool',...
    'ClickedCallback', 'pan');

% [zoomInBtn] - zoom in button
uipushtool(...
    'Parent',          tb,...
    'Tag',             'zoomInBtn',...
    'CData',           zoomInIcon,...
    'TooltipString',   'zoom in tool',...
    'ClickedCallback', 'zoom');

% [zoomOutBtn] - zoom out button (just resets zoom settings)
uipushtool(...
    'Parent',          tb,...
    'Tag',             'zoomOutBtn',...
    'CData',           zoomOutIcon,...
    'TooltipString',   'zoom out to initial zoom setting',...
    'ClickedCallback', 'zoom out');

% [speed1 Static]
uicontrol(...
    'Parent',          fig,...
    'Tag',             'r1Static',...
    'Style',           'text',...
    'String',          'Speed 1 :',...
    'FontSize',        12,...
    'HorizontalAlignment', 'right',...
    'Units',           'normalized',...
    'Position',        [.65 .9 .1 .05]);

% [speed2 Static]
uicontrol(...
    'Parent',          fig,...
    'Tag',             'r2Static',...
    'Style',           'text',...
    'String',          'Speed 2 :',...
    'FontSize',        12,...
    'HorizontalAlignment', 'right',...
    'Units',           'normalized',...
    'Position',        [.65 .8 .1 .1]);

% [x Start Position Static]
uicontrol(...
    'Parent',          fig,...
    'Tag',             'xstartPStatic',...
    'Style',           'text',...
    'String',          'X Start Coordinate :',...
    'FontSize',        12,...
    'HorizontalAlignment', 'right',...
    'Units',           'normalized',...
    'Position',        [.6 .75 .15 .1]);

% [y Start Position Static]
uicontrol(...
    'Parent',          fig,...
    'Tag',             'ystartPStatic',...
    'Style',           'text',...
    'String',          'Y Start Coordinate :',...
    'FontSize',        12,...
    'HorizontalAlignment', 'right',...
    'Units',           'normalized',...
    'Position',        [.6 .7 .15 .1]);

% [Time Static]
uicontrol(...
    'Parent',          fig,...
    'Tag',             'timeStatic',...
    'Style',           'text',...
    'String',          'Time :',...
    'FontSize',        12,...
    'HorizontalAlignment', 'right',...
    'Units',           'normalized',...
    'Position',        [.65 .65 .1 .1]);

% [speed1]
uicontrol(...
    'Parent',          fig,...
    'Tag',             'speed1',...
    'Style',           'edit',...
    'String',          '0',...      % initial value
    'Units',           'normalized',...
    'Position',        [.75 .9 .15 .05]);

% [speed2]
uicontrol(...
    'Parent',          fig,...
    'Tag',             'speed2',...
    'Style',           'edit',...
    'String',          '0',...      % initial value
    'Units',           'normalized',...
    'Position',        [.75 .85 .15 .05]);

% [x start position]
uicontrol(...
    'Parent',          fig,...
    'Tag',             'xstartP',...
    'Style',           'edit',...
    'String',          '0',...      % initial value
    'Units',           'normalized',...
    'Position',        [.75 .8 .15 .05]);

% [y start position]
uicontrol(...
    'Parent',          fig,...
    'Tag',             'ystartP',...
    'Style',           'edit',...
    'String',          '0',...      % initial value
    'Units',           'normalized',...
    'Position',        [.75 .75 .15 .05]);

% [time]
uicontrol(...
    'Parent',          fig,...
    'Tag',             'time',...
    'Style',           'edit',...
    'String',          '0',...      % initial value
    'Units',           'normalized',...
    'Position',        [.75 .7 .15 .05]);

%run button
uicontrol(...
    'Parent',       fig,...
    'Tag',             'runBtn',...
    'Style',           'pushbutton',...
    'String',          'Run Simulation',...
    'FontSize',        12,...
    'FontWeight',      'bold',...
    'Units',           'normalized',...
    'Position',        [.45 .05 .15 .1],...
    'Callback',        @run_button_Callback);

% [axes] - add axes for plot
axes(...
    'Parent',          fig,...
    'Tag',             'axes',...
    'Units',           'normalized',...
    'Position',        [.05 .4 .5 .5]);

%need to comment the algorithm
%ultimately want to show feasible set
function run_button_Callback(hObject,callbackdata)
    data = guidata(hObject);
    handles = guihandles;
    %turn buttons off while running
    allEnabled = findobj(handles.fig,'Enable','on');
    set(allEnabled,'Enable','off');
    
    %grab the old value of the button string
    oldVal = hObject.String;
    %change string to running
    hObject.String = 'Running...';
    drawnow;
    
    %get the input arguments
    r1 = str2double(handles.speed1.String); %speed in first region
    r2 = str2double(handles.speed2.String); %speed in second region
    xstartP = str2double(handles.xstartP.String); %x-coordinate of starting position
    ystartP = str2double(handles.ystartP.String); %y-coordinate of start position
    time = str2double(handles.time.String); %time to travel
    
    x1max = sqrt((r1*time)^2-ystartP^2);
    points = linspace(xstartP-x1max,xstartP+x1max,100);
    for i = 1:length(points)
        timeLeft(i) = time - sqrt((points(i)-xstartP)^2+ystartP^2)/r1;
        x2max(i) = r2*timeLeft(i);
    end
    
    
    %get the current figure
    curFig = gcf;
    cla;
    j=1;
    th = linspace( pi, 0, 100); %theta
    %parameterize and plot the feasible set in second region
    for i = 1:length(points)
        R = x2max; %radius
        x = R(i)*cos(th) + points(i);
        y = R(i)*sin(th);
        j = j+1;
        plot(x,y); axis equal;
        hold on;
    end
    %plot the feasible set in first region
    %acos returns radians
    normalAngle = acos(abs(ystartP)/(r1*time)); %angle between path to xmax and x = 0
    angles = linspace( pi/2 + normalAngle, 5*pi/2 - normalAngle, 100); %discretize angles
    feasibleDist = r1*time; %radial distance reachable from start point
    x = feasibleDist*cos(angles) + xstartP; %x coordinate
    y = feasibleDist*sin(angles) + ystartP; %y coordinate
    plot(x,y);
    hold on;
    %refline adds a reference line to the plot
    refline(0,0)
        
    hObject.String = oldVal;
        
    % reenable all gui elements
    set(allEnabled,'Enable','on');

    
    
    

