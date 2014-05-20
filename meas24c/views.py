# Create your views here.
from meas24c.models import ChargedMeson24c

ps_mesons_005 = ChargedMeson24c.objects.filter(source='GFWALL', sink='GAM_5',
                                               m_l=0.005)

ps_mesons_01 = ChargedMeson24c.objects.filter(source='GFWALL', sink='GAM_5',
                                              m_l=0.01)

ps_mesons_02 = ChargedMeson24c.objects.filter(source='GFWALL', sink='GAM_5',
                                              m_l=0.02)

ps_mesons_03 = ChargedMeson24c.objects.filter(source='GFWALL', sink='GAM_5',
                                              m_l=0.03)

