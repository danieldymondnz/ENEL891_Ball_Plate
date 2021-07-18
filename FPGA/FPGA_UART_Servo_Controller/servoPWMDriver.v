module servoPWMDriver( 	input [6:0] position,
								input clk,
								output reg pulse );
	
	reg [8:0] counter, mark;
		
	always@ (posedge clk)	begin
	
			// 360 ticks per frame
			if (counter > 359)
				counter = 9'b0;
			else 
				counter = counter + 1;

			// 
			if (mark > counter)
				pulse = 1'b1;
			else
				pulse = 1'b0;
				
			// Update Mark with new Input Data + 116
			mark = position + 116;
	end
						
endmodule 