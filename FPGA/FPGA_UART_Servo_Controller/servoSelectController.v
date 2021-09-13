module servoSelectController( input [7:0] rxData, input newData,
										output reg [6:0] xPWM,yPWM);
						
	reg [6:0] xPWMStore;
	reg [6:0] yPWMStore;
						
	always @(posedge newData) begin

		if (rxData[7] == 1'b0) begin
			xPWMStore = rxData[6:0]
		end
		else begin
			yPWMStore = rxData[6:0]
		end
		
		// Regardless, output current values for x & y PWM
		xPWM = xPWMStore;
		yPWM = yPWMStore;
			
	end
						
										
endmodule 