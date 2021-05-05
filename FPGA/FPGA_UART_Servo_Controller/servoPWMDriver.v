module servoPWMDriver( 	input [6:0] position,
								input clk,
								output reg pulse );
	
	reg [12:0] counter, mark;
		
	always@ (posedge clk)	begin
	
			// 2500 pwmClk Ticks = 20ms or 1 period
			if (counter > 2559)
				counter = 0;
			else 
				counter = counter + 1'b1;

			// 
			if (mark > counter)
				pulse = 1'b1;
			else
				pulse = 1'b0;
				
			// Update Mark with new Input Data
			mark = position + 7'b1111111;
	end
						
endmodule 