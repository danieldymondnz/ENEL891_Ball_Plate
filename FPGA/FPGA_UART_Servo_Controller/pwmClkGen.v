module pwmClkGen (input clk50MHz,
						output reg pwmClk);
						
	reg [7:0] count;
		
		always @ (posedge clk50MHz) begin
			
			// Servo operates at 333Hz
			// For 0.5 degree resolution over 180*, totals 360 ticks per frame
			// 50 / (360 * 333 * 2) - 1 = 208
			if (count > 208) begin
				count = 8'd0;
				pwmClk = !pwmClk;
			end
			else
				count = count + 8'd1;
		end
		
endmodule 