module servoSelectController( input [7:0] rxData,
										output reg [6:0] xPWM,yPWM);
						
	always @ (*) begin
			if(rxData[7] == 1)
				xPWM = {rxData[6:0]};
			else
				yPWM = {rxData[6:0]};
	end
						
										
endmodule 