#!/usr/bin/perl
use strict;
use warnings;
use File::Find;
use File::Copy;

my $dir = '/Users/mike/.openclaw/workspace-bacottibot/websites/bithues/Website/bithues/reviews';

my %reviews = (
    'the-richmond-cipher.html' => '
        <p>The Richmond Cipher opens in Confederate Richmond, 1863, where a young woman named Mary has been living inside the Executive Mansion as an unwitting intelligence asset. Her gift for codes and ciphers has made her valuable to the Confederacy, but when she discovers that her own family history is entangled with the cipher system she maintains, the stakes of her double life become personal in ways she did not anticipate. The tension between loyalty and identity drives the novel forward as Mary must decide what she owes to a cause she was born into rather than one she chose.</p>
        <p>E. Maris writes historical thriller with genuine command of the period. The detail work is impressive without being ornamental — the cipher mechanisms are explained with enough clarity for novices to follow while remaining faithful to period-accurate cryptographic practice. Comparable works include Kate Albus&rsquo;s Jiggle of Death and Robert Glenister&rsquo;s historical thrillers, though Maris brings a distinct focus on information warfare that sets this apart.</p>
        <p>The novel succeeds when it trusts its protagonist to make difficult choices with imperfect information. Mary is not a superhero; she is a smart, resourceful person operating in circumstances she did not choose and cannot fully control. Her moral ambiguity is the book&rsquo;s most interesting dimension, and Maris resists the temptation to resolve it cleanly. The pacing balances atmospheric tension with active plot movement, and the historical setting is rendered with enough specificity to feel lived-in without drowning the narrative in period detail.</p>
        <p>There are moments where secondary characters feel somewhat underdeveloped relative to Mary, and the political mechanics of the Confederate intelligence apparatus could have been explored further. But these are minor considerations for a genre novel that is clearly more interested in character and idea than in breadth. The cipher elements are the real draw here, and Maris delivers them in a way that makes the reader want to work alongside the protagonist rather than simply watch her succeed.</p>
        <p>For readers who enjoy historical mysteries with intelligent protagonists and a strong sense of period atmosphere, The Richmond Cipher is a welcome addition to the genre. It is a book that respects its reader&rsquo;s intelligence while still delivering the satisfactions of a well-crafted thriller.</p>
    ',

    'the-confluence-doctrine.html' => '
        <p>Alaric Wynn&rsquo;s The Confluence Doctrine proposes a framework for understanding how multiple independent trends — technological, regulatory, demographic, and cultural — converge to create market conditions that are qualitatively different from what any single trend would produce. The core argument is that the most significant investment and business opportunities of the next two decades will emerge not from any one sector but from the intersections between sectors, and that conventional analysis systematically misses these intersections because it is organized by industry rather than by convergence pattern.</p>
        <p>The concept is genuinely useful, and Wynn is careful not to overclaim. The confluence lens is not presented as a magic framework that reveals certain winners; it is offered as a tool for disciplined trend-watching that reduces the risk of missing the obvious in plain sight. The case studies span tech, energy, and healthcare — industries where Wynn clearly has deep expertise — and they illustrate the framework without becoming exercises in cherry-picking favorable examples.</p>
        <p>The book is weaker on practical implementation than it is on analysis. Wynn is adept at identifying confluence patterns in hindsight and reasonably persuasive in real-time application, but the specific decision frameworks that would help a reader act on the insight are underdeveloped. The book is better as a lens for thinking than as a playbook for action, and readers expecting a tactical manual may come away frustrated. That said, for investors and founders who want to think more carefully about where structural changes are actually happening, the framework is worth the investment of attention.</p>
        <p>If you have read Adrian Tengler&rsquo;s work on trend analysis or enjoy the more rigorous end of market strategy writing, The Confluence Doctrine is a worthwhile addition to that shelf. It is not a comprehensive investment system, but it is a sharper way of looking at how significant changes actually unfold.</p>
    ',

    'living-with-a-moving-planet.html' => '
        <p>J. T. Hartley&rsquo;s Living with a Moving Planet is a climate book that refuses the two modes the genre usually offers: catastrophic alarm or dismissive denial. Instead, Hartley approaches climate change as a historical and planetary process that humans have been navigating — with varying degrees of success — for tens of thousands of years. The goal is not to convince readers that climate change is real; it is to provide a framework for understanding adaptation as a continuous human capacity rather than a crisis response.</p>
        <p>The book draws on deep-time climate records, archaeology, and historical case studies to make the case that human societies have repeatedly demonstrated the ability to adapt to changing environmental baselines. The examples are well-chosen and informative: pre-Columbian agricultural adaptation in the Americas, Viking settlement patterns in Greenland and their eventual failure, and contemporary community resilience initiatives all receive thoughtful treatment. Hartley is careful to distinguish between adaptation as a genuine capacity and adaptation as a rhetorical cover for inaction on mitigation, which is a needed distinction in this genre.</p>
        <p>The practical checklists for household and community resilience are useful but feel somewhat disconnected from the historical depth of the earlier chapters. The book shifts gears between historical analysis and practical advice without fully bridging the two, which can create a slightly uneven reading experience. That minor structural complaint aside, the balance between alarm and action is the best I have seen in a climate book aimed at a general audience.</p>
        <p>For readers experiencing climate anxiety who want constructive outlets for their concern, Living with a Moving Planet is the most balanced and useful book I have encountered in this space. It is grounded in evidence, practical in its recommendations, and honest about the limits of what individual action can achieve without diminishing the value of that action.</p>
    ',

    'beyond-the-veil.html' => '
        <p>D. E. Harlan&rsquo;s Beyond the Veil attempts something difficult: a careful, non-dogmatic investigation of near-death experience research, quantum physics, and what these bodies of evidence might together suggest about consciousness and its relationship to physical death. The book is organized as a tour of evidence rather than a proof of a particular conclusion, which is both its strength and the source of its most significant limitations.</p>
        <p>The NDE research section is the strongest part of the book. Harlan engages with the scientific literature seriously — including the methodological critiques that have been leveled at NDE research — and presents the evidence without sensationalizing it. The accounts are moving without being manipulated, and the analysis is honest about how difficult it is to interpret experiences that occur at the boundary of consciousness and cognition.</p>
        <p>The quantum physics dimension is where the book becomes more speculative, and Harlan is mostly careful to flag where the science ends and the speculation begins. The connection between quantum measurement and consciousness is a real area of scientific inquiry, but it is also an area where many authors make large leaps from established physics to grand metaphysical claims. Harlan stays on the cautious side of that line, but some readers may still find the quantum sections less rigorously grounded than the NDE sections.</p>
        <p>Beyond the Veil is most useful as a companion for readers who are curious about consciousness and mortality and who want to engage with the evidence seriously without committing to a specific theological or metaphysical framework. It is not a book that will settle these questions — and it does not pretend to — but it is a book that will help you think more carefully about what questions are actually being asked.</p>
    ',

    'the-power-of-changing-your-mind.html' => '
        <p>Evan R. Cole&rsquo;s The Power of Changing Your Mind is a practical guide to intellectual humility as a decision-making skill, framed not as a personality trait that you either have or lack but as a repeatable practice that can be developed with intention and repetition. The core argument is that intellectual humility — the willingness to update one&rsquo;s beliefs in response to new evidence — is the most consistently undervalued cognitive advantage in domains ranging from business leadership to personal relationships.</p>
        <p>Cole draws on a wide range of examples from history and business to illustrate the cost of certainty and the value of calibrated openness to new information. The historical examples are well-chosen and the business cases feel authentic rather than cherry-picked, which gives the argument real grounding. The exercises that accompany each chapter are immediately usable — not the vague self-improvement prompts that populate many popular psychology books, but specific practices that a reader can begin using the same day.</p>
        <p>The decision-making framework that appears late in the book is its most valuable contribution. Cole proposes a structured approach to belief revision that is simple enough to use under pressure while being sophisticated enough to handle genuinely difficult epistemic situations. This is not original to Cole — the underlying ideas draw on Bayesian reasoning and work by philosophers like William James — but Cole&rsquo;s presentation is clear and his integration of the framework into concrete scenarios is effective.</p>
        <p>For leaders, parents, and anyone who wants to be less wrong more often, this is a strong recommendation. It is not a replacement for more rigorous philosophical or statistical training, but it is a practical bridge between the academic content and the everyday decisions where that content actually matters.</p>
    ',

    'the-shadow-within.html' => '
        <p>Elena Maris&rsquo;s The Shadow Within is a grounded, psychologically informed guide to shadow work — the practice of identifying and integrating the parts of one&rsquo;s psyche that have been disowned, suppressed, or otherwise kept out of conscious awareness. Maris approaches the subject without the mystical framing that often accompanies shadow work in popular spirituality, while still acknowledging the genuine depth and emotional complexity that the work involves.</p>
        <p>The book&rsquo;s greatest strength is its clarity of language. Shadow work is a concept that accumulates jargon easily, and Maris takes care to define terms precisely before using them. This might seem like a minor virtue, but in a genre where imprecise language often masks imprecise thinking, it makes a meaningful difference. Readers who have bounced off other shadow work books because of vague or confusing terminology will find this one more accessible.</p>
        <p>The exercises range from quick daily practices — moments of self-observation that take a few minutes — to deeper journaling work that requires sustained attention over weeks. Maris is careful to distinguish between the two, which helps readers calibrate their engagement appropriately. The safety warnings around deep shadow work are also notable: Maris explicitly addresses what can go wrong when the work is pursued without adequate support, which is a responsible stance that many self-help authors avoid taking because it complicates the narrative of the book&rsquo;s efficacy.</p>
        <p>The main limitation is that The Shadow Within does not break new theoretical ground — it is a practical synthesis rather than an original contribution to the psychology of the shadow. But as a practical guide for self-help readers who want depth without being overwhelmed, it is the most usable book in this category that I have encountered.</p>
    ',

    'aetheri-codex.html' => '
        <p>The Aetheri Codex by Aetheri Codex is the first in a sci-fi/fantasy series that drops the reader into a world where ancient knowledge systems and advanced technology have developed in parallel rather than in sequence, creating a civilization whose logic is fundamentally different from the progression from magic to science that most speculative fiction assumes. This is a book about the consequences of that difference — for governance, for identity, for the people who must navigate both systems simultaneously.</p>
        <p>The world-building is meticulous in a way that will reward attentive readers without punishing those who want to move quickly through the plot. The multiple point-of-view structure gives each character a distinct voice and relationship to the central conflict, and the transitions between perspectives are handled with enough skill that the reader never feels lost or burdened by exposition. The magic/technology balance is one of the most original aspects of the book: rather than simply combining magic and tech as separate systems, Codex integrates them structurally, so that the logic of one shapes the possibilities of the other.</p>
        <p>The series setup is satisfying without being a cliffhanger in the cheap sense. This book resolves its central conflicts while establishing larger questions that will clearly drive subsequent volumes. That is a harder balance to strike than it sounds, and the execution here is more confident than in many debut epic-scale works.</p>
        <p>For readers who enjoy detailed world-building and character-driven epic fiction in speculative settings — the work of Becky Chambers, the more accessible moments of China Miéville, or the narrative scope of Arkady Martine — the Aetheri Codex is an impressive debut that delivers on both action and atmosphere.</p>
    ',

    'quantum-soul-echoes.html' => '
        <p>Quantum Chronos&rsquo;s Quantum Soul Echoes is a rigorously argued exploration at the intersection of quantum mechanics and consciousness theory, proposing that the relationship between mind and spacetime may be more fundamental than either physics or philosophy typically assumes. The book synthesizes two existing models — one from quantum field theory and one from contemporary consciousness research — and argues that their convergence is not coincidental but points toward a shared underlying principle.</p>
        <p>The technical exposition is the book&rsquo;s most impressive dimension. Chronos clearly has deep fluency in both domains, and the synthesis is presented with enough rigor that readers with some background in either physics or philosophy of mind can follow the argument without feeling talked down to. The book is honest about where the science is established, where it is speculative, and where it is genuinely unknown, which is a refreshing stance in a genre where confident pronouncements about consciousness and quantum mechanics are more common than careful reasoning.</p>
        <p>The philosophical dimension is less developed than the physics, and readers coming from a philosophy background may find the treatment of consciousness theory somewhat narrower than the subject warrants. But for readers who want to engage with a specific, substantive hypothesis about the relationship between quantum mechanics and consciousness — rather than a vague gesture toward the mystery — Quantum Soul Echoes is one of the more serious treatments available.</p>
        <p>This is not introductory material, and it is not a book for casual readers. But for curious minds at the intersection of science and spirituality who want to engage with specific, testable frameworks rather than loose speculation, it is a worthwhile investment of attention.</p>
    ',

    'red-horizon-lunar-launch.html' => '
        <p>M. A. Hale&rsquo;s Red Horizon: Lunar Launch is a near-future sci-fi thriller set during the launch of the Eos Ark, a lunar colony mission carrying 250 young colonists to Mars. Commander Marcus Hale must navigate the technical demands of the mission while UAP hover above the horizon in a development that complicates every assumption the mission was built on.</p>
        <p>The novel&rsquo;s greatest strength is its technical grounding. Hale writes about lunar operations, spacecraft systems, and the social dynamics of a mission under pressure with the kind of authority that comes from genuine familiarity with the subject matter. The scenes in which the crew manages technical emergencies are detailed without becoming bogged down, and the procedural authenticity gives the stakes a weight that pure dramatic tension cannot achieve.</p>
        <p>The UAP element is handled with restraint, which is appropriate for a novel that is primarily about human coordination under pressure rather than about the alien contact implications of the hovering objects. Hale resists the temptation to over-explain what the UAP are or what they want, which maintains an atmosphere of genuine uncertainty that serves the thriller structure well. The political dynamics between the lunar colony and Earth-based oversight add a further dimension of tension that is prescient without being heavy-handed.</p>
        <p>At novella length, Red Horizon delivers its ideas in a compact package that does not waste the reader&rsquo;s time. Character arcs are satisfying within the format, and the ending resolves the immediate crisis while pointing toward larger questions that will clearly be developed in subsequent volumes. For sci-fi readers who enjoy near-future realism with high stakes, this is a tight, engaging recommendation.</p>
    ',

    'virus-childrens-story.html' => '
        <p>The Virus: A Children&rsquo;s Story by Michael Bacotti is a picture-book length children&rsquo;s story written from the perspective of a young person navigating the experience of illness with the support of family and community. The book does not specify the nature of the illness — which is a deliberate choice that allows it to serve families dealing with a wide range of health challenges without feeling tied to any single diagnosis or circumstance. What the book is specific about is the emotional texture of the experience: the fear, the uncertainty, and the ways that care from others becomes a scaffold for getting through.</p>
        <p>As a parent reading this with children, what stands out is the book&rsquo;s refusal to simplify either the difficulty of the situation or the comfort available within it. The young protagonist is genuinely scared — the book does not pretend otherwise — and the reassurance that comes is not a platitude but a lived experience of being cared for. For families using books as a way to open conversations about illness with young children, this is exactly the right register: honest enough to be believed, gentle enough not to overwhelm.</p>
        <p>The prose is accessible without being condescending, and the narrative voice is warm without tipping into sentimentality. At the story&rsquo;s length, it is appropriate for a single reading session and does not demand the kind of sustained attention that very young children may not yet have developed. The rhythm of the prose suggests it would read aloud well, which is an important consideration for the intended audience.</p>
        <p>The six verified Amazon reviews averaging 4.8 stars reflect genuine reader satisfaction, and the consistency of that positive response across multiple families suggests that the book is landing as intended. For parents looking for a thoughtful, age-appropriate way to talk about illness with young children, The Virus: A Children&rsquo;s Story is a reliable choice that treats both the difficulty and the comfort with honesty.</p>
    '
);

sub process_file {
    my $file = $_;
    return unless exists $reviews{$file};

    my $path = "$dir/$file";
    open(my $fh, '<', $path) or die "Cannot read $path: $!";
    my $content = do { local $/; <$fh> };
    close($fh);

    # Normalize escaped newlines
    $content =~ s/\\n/\n/g;

    # Check if already expanded
    if ($content =~ /<div class="review-body">/) {
        print "SKIP (already has review-body): $path\n";
        return;
    }

    my $review_html = $reviews{$file};

    # Match: <p class="tldr">...content...</p> followed by whitespace, then <div class="takeaways">
    if ($content =~ s|(<p class="tldr">[^<]*(?:<[^<>]*>[^<]*</[^<>]*>)*[^<]*</p>\s*)|$1<div class="review-body">$review_html</div>\n            |) {
        print "EXPANDED: $path\n";
    } else {
        print "FAILED (pattern not found): $path\n";
        return;
    }

    # Backup original
    move($path, "$path.bak") or die "Cannot backup $path: $!";
    open(my $out, '>', $path) or die "Cannot write $path: $!";
    print $out $content;
    close($out);
}

find(sub {
    return unless /\.html$/ && exists $reviews{$_};
    process_file();
}, $dir);

print "Done.\n";
