
$(document).ready(function() {

        /** 
        ** Draw a sparkline showing current kw usage
        ** and then updates the display a couple of times a second via
        ** setTimeout()
        **/
	var mrefreshinterval = 250; // update display every 500ms
	var kwpoints = [];
	var kvapoints = [];
	var vpoints = [];
	var pfpoints = []; 
	var timepoints = [];
	var lasttime = "";
	
	var mpoints_max = 60*3; // was 120
	var kwmin = 10000000.0;
	var kwmax = 0.0;
	var vmin = 10000000.0;
	var vmax = 0.0;
	var kvamin = 10000000.0;
	var kvamax = 0.0;
	var pfmin = 1.0;
	var pfmax = 0.0;
	
	var linecolor = '#155811';
	var fillcolor = '#b4ecb4';
	var maxcolor = '#42b1ef';
	var mincolor = '#42b1ef';
	var spotcolor = '#ff3333';
	
	Array.max = function( array ){
		return Math.max.apply( Math, array );
	};

	Array.min = function( array ){
		return Math.min.apply( Math, array );
	};
	dataget = function() {
		var kw = 0.0;
		var kva = 0.0;
		var volt = 0.0;
		$.getJSON("/electric/livedata/data", function(data) {
			time = data.time;
			if (lasttime !== time) {
				kw = parseFloat(data.power);
				kva = parseFloat(data.kva);
				volt = parseFloat(data.voltage);
                                powerfactor = Math.round(kw / kva * 1000)/1000;
				
				// prepare power...
				kwpoints.push(kw);
				if (kwpoints.length > mpoints_max)
					kwpoints.splice(0,1);
				kwmax = Array.max(kwpoints)
				kwmin = Array.min(kwpoints)
					$('#kwSparkline').sparkline(kwpoints, { 
						width: kwpoints.length*2, 
						height: '30px', 
						lineColor:linecolor, 
						fillColor:fillcolor,
						minSpotColor:mincolor,
						maxSpotColor:maxcolor,
						spotColor: spotcolor,
						defaultPixelsPerValue:1});
				$('#kwFirst').html(kwpoints[0]);
				$('#kwBox').html(kw);
				$('#kwMin').html(kwmin);
				$('#kwMax').html(kwmax);
				
				// prepare kva...
				kvapoints.push(kva);
				if (kvapoints.length > mpoints_max)
					kvapoints.splice(0,1);
				kvamax = Array.max(kvapoints)
				kvamin = Array.min(kvapoints)
					$('#kvaSparkline').sparkline(kvapoints, { 
						width: kvapoints.length*2, 
						height: '30px', 
						lineColor:linecolor, 
						fillColor:fillcolor,
						minSpotColor:mincolor,
						maxSpotColor:maxcolor,
						spotColor: spotcolor,
						defaultPixelsPerValue:1});
				$('#kvaFirst').html(kvapoints[0]);
				$('#kvaBox').html(kva);
				$('#kvaMin').html(kvamin);
				$('#kvaMax').html(kvamax);
			
				
				// prepare voltage...
				vpoints.push(volt);
				if (vpoints.length > mpoints_max)
					vpoints.splice(0,1);
				vmax = Array.max(vpoints)
				vmin = Array.min(vpoints)
					$('#vSparkline').sparkline(vpoints, { 
						width: vpoints.length*2, 
						height: '30px', 
						lineColor:linecolor, 
						fillColor:fillcolor,
						minSpotColor:mincolor,
						maxSpotColor:maxcolor,
						spotColor: spotcolor,
						defaultPixelsPerValue:1});
				$('#voltFirst').html(vpoints[0]);
				$('#voltBox').html(volt);
				$('#voltMin').html(vmin);
				$('#voltMax').html(vmax);

                                // prepare power factor...
                                pfpoints.push(powerfactor);
                                if (pfpoints.length > mpoints_max)
                                        pfpoints.splice(0,1);
                                pfmax = Array.max(pfpoints)
                                pfmin = Array.min(pfpoints)
                                        $('#pfSparkline').sparkline(pfpoints, {
                                                width: pfpoints.length*2,
                                                height: '30px',
                                                lineColor:linecolor,
                                                fillColor:fillcolor,
                                                minSpotColor:mincolor,
                                                maxSpotColor:maxcolor,
                                                spotColor: spotcolor,
                                                defaultPixelsPerValue:1});
                                $('#pfFirst').html(pfpoints[0]);
                                $('#pfBox').html(powerfactor);
                                $('#pfMin').html(pfmin);
                                $('#pfMax').html(pfmax);

				// prepare time...
				timepoints.push(time);
				if (timepoints.length > mpoints_max)
					timepoints.splice(0,1);
				$('#currTimeBox').html(time);
				$('#FirstTimeBox').html(timepoints[0]);
				
				lasttime = time
			}
			
			mtimer = setTimeout(dataget, mrefreshinterval);
		});
	}
	var mtimer = setTimeout(dataget, mrefreshinterval);
});
