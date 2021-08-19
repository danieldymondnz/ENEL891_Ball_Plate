module pwmClkGen (input clk50MHz,
						output reg pwmClk);
						
	reg [4:0] count;
		
		always @ (posedge clk50MHz) begin
			
			// Servo operates at 333Hz
			// For 1024 bits resolution over 40*, totals 4608 ticks/frame
			// 50 / (4608 * 333) = 37
			if (count > 18) begin
				count = 5'd0;
				pwmClk = !pwmClk;
			end
			else
				count = count + 5'd1;
		end
		
endmodule 