module rxIndicator( input rxFlag, baudClk,
					output reg rxLED);
					
		reg [10:0] count;
					
		always@ (posedge baudClk) begin
		
			if (rxFlag) 
				count = 1920;
			
			if (count > 0) begin
				count = count - 11'b1;
				rxLED = 1'b1;
			end
			else
				rxLED = 1'b0;		
		
		end

endmodule 