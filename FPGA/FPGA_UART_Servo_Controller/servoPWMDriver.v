module servoPWMDriver( 	input [6:0] position,
								input clk,
								output reg pulse );
	
	reg [6:0] counter, mark;
		
	always@ (posedge clk)	begin
	
			// 2500 pwmClk Ticks = 20ms or 1 period
			// was 2559
			if (counter > 127)
				counter = 1'b0;
			else 
				counter = counter + 1'b1;

			// 
			if (mark > counter)
				pulse = 1'b1;
			else
				pulse = 1'b0;
				
			// Update Mark with new Input Data
			mark = position; // + 7'b1111111;
	end
						
endmodule 