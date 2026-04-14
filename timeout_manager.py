
from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3


class FinalController(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(FinalController, self).__init__(*args, **kwargs)
        self.blocked_once = False

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        dp = ev.msg.datapath
        parser = dp.ofproto_parser
        ofproto = dp.ofproto

        # Table-miss rule → send packets to controller
        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(
            ofproto.OFPP_CONTROLLER,
            ofproto.OFPCML_NO_BUFFER
        )]

        inst = [parser.OFPInstructionActions(
            ofproto.OFPIT_APPLY_ACTIONS, actions)]

        dp.send_msg(parser.OFPFlowMod(
            datapath=dp,
            priority=0,
            match=match,
            instructions=inst
        ))

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def packet_in_handler(self, ev):
        msg = ev.msg
        dp = msg.datapath
        parser = dp.ofproto_parser
        ofproto = dp.ofproto

        in_port = msg.match['in_port']

        
        if in_port == 1 and not self.blocked_once:
            self.logger.info("BLOCKING h1 TRAFFIC")

            dp.send_msg(parser.OFPFlowMod(
                datapath=dp,
                priority=10,
                match=parser.OFPMatch(in_port=1),
                instructions=[],  
                hard_timeout=10,
                flags=ofproto.OFPFF_SEND_FLOW_REM  
            ))

            self.blocked_once = True
            return

       
        actions = [parser.OFPActionOutput(ofproto.OFPP_FLOOD)]

        dp.send_msg(parser.OFPPacketOut(
            datapath=dp,
            buffer_id=ofproto.OFP_NO_BUFFER,
            in_port=in_port,
            actions=actions,
            data=msg.data
        ))

 
    @set_ev_cls(ofp_event.EventOFPFlowRemoved, MAIN_DISPATCHER)
    def flow_removed_handler(self, ev):
        self.logger.info("FLOW EXPIRED")

