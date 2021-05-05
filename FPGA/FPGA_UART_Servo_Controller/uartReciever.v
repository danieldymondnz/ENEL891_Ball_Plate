module uartReciever(input clk, rxIn,
							output reg [7:0] rxData, output reg rxCompleteFlag);

reg [3:0] baudCount, state;
reg [7:0] rxDataTemp;

parameter [3:0] 
	idle 		= 4'd0,
	startBit = 4'd1,
	bit0 		= 4'd2,
	bit1 		= 4'd3,
	bit2 		= 4'd4,
	bit3 		= 4'd5,
	bit4 		= 4'd6,
	bit5 		= 4'd7,
	bit6 		= 4'd8,
	bit7 		= 4'd9,
	stopBit 	= 4'd10;
	
	
	always @( posedge clk) begin
		baudCount = baudCount + 1'b1;
		
		case(state)
			idle: begin
						rxCompleteFlag = 0;
						if (rxIn == 0) begin
							state = startBit;
							baudCount = 0;
						end
			
					end
		
			startBit: begin
							if((baudCount == 7) && (rxIn == 1) )
								state = idle;
							else if (baudCount == 15)
								state = bit0;
			
						end
			
			bit0: begin
						if(baudCount == 7)
							rxDataTemp[0] = rxIn;						
						else if (baudCount == 15)
								state = bit1;		
					end
				
			bit1: begin
						if(baudCount == 7)
							rxDataTemp[1] = rxIn;						
						else if (baudCount == 15)
								state = bit2;		
					end
			bit2: begin
						if(baudCount == 7)
							rxDataTemp[2] = rxIn;						
						else if (baudCount == 15)
								state = bit3;		
					end
					
			bit3: begin
						if(baudCount == 7)
							rxDataTemp[3] = rxIn;						
						else if (baudCount == 15)
								state = bit4;		
					end
					
			bit4: begin
						if(baudCount == 7)
							rxDataTemp[4] = rxIn;						
						else if (baudCount == 15)
								state = bit5;		
					end		

			bit5: begin
						if(baudCount == 7)
							rxDataTemp[5] = rxIn;						
						else if (baudCount == 15)
								state = bit6;		
					end	
					
			bit6: begin
						if(baudCount == 7)
							rxDataTemp[6] = rxIn;						
						else if (baudCount == 15)
								state = bit7;		
					end
				
			bit7: begin
						if(baudCount == 7)
							rxDataTemp[7] = rxIn;						
						else if (baudCount == 15)
								state = stopBit;		
					end	

			stopBit: begin
							if (baudCount == 15) begin
								state = idle;	
								rxCompleteFlag = 1;
								rxData = rxDataTemp;
							end
						end				
				
		endcase
	
	
	
	end


endmodule 