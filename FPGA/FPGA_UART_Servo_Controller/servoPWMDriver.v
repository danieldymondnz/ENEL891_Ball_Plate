module servoPWMDriver( 	input [7:0] position,
								input clk,
								output reg pulse );
	
	reg [14:0] counter, mark;
		
	always@ (posedge clk)	begin
	
			if (counter > 20_000)
				counter = 0;
			else 
				counter = counter + 1'b1;


			if (mark > counter)
				pulse = 1'b1;
			else
				pulse= 1'b0;
				
				mark = position * 4;
	end
						
endmodule 