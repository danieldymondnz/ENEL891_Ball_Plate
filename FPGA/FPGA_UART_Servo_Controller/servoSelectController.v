module servoSelectController( input [7:0] rxData, input newData,
										output reg [9:0] xPWM,yPWM);
						
	reg [9:0] xPWMStore;
	reg [9:0] yPWMStore;
	reg [4:0] highData;
	reg [4:0] lowData;
	reg lastServoWrite;
	reg currServoWrite;
	
	initial lastServoWrite = 1'b1;
						
	always @(posedge newData) begin
	
		// Set Servo Flag
		if (rxData[7:5] == 3'b000) begin
			currServoWrite = 1'b0;
		end
		else begin
			currServoWrite = 1'b1;
		end
		
		// If last servo write is same as current, then extract data in last 5 positions
		if (lastServoWrite == currServoWrite) begin
			lowData = rxData[4:0];
		end
		else begin
			highData = rxData[4:0];
		end
		
		// If both high and low data is determined, write the data to the applicable datastore
		if (lastServoWrite == currServoWrite) begin
			
			if (currServoWrite == 1'b0) begin
				xPWMStore[9:5] = highData;
				xPWMStore[4:0] = lowData;
			end
			else begin
				yPWMStore[9:5] = highData;
				yPWMStore[4:0] = lowData;
			end
			
		end
		
		// Regardless, output current values for x & y PWM
		xPWM = xPWMStore;
		yPWM = yPWMStore;
		
		// Shuffle Servo Flag for next comparision
		lastServoWrite = currServoWrite;
			
	end
						
										
endmodule 