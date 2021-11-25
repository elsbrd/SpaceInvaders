(import [numpy :as np]
        [dataclasses [dataclass]]
)

(with-decorator (dataclass :eq False)
  (defclass Vector []
    (setv ^int x 0)
    (setv ^int y 0)

    (defn manhattan [self ^"Vector" other]
      (+ (abs (- self.x other.x)) (abs (- self.y other.y)))
    )
    (defn copy [self]
      (Vector self.x self.y)
    )
    (defn __add__ [self ^"Vector" other]
      (Vector (+ self.x other.x) (+ self.y other.y))
    )
    (defn __eq__ [self ^"Vector" other]
      (and (= self.x other.x) (= self.y other.y))
    )
    (defn __iter__ [self]
      (gfor coord (, self.x self.y) coord)
    )
  )
)

(setv Position Vector)
(setv Labyrinth np.ndarray)
(setv Cost float)
(setv Agent int)

(defclass Move []
  (setv DOWN (Vector 0 1))
  (setv LEFT (Vector -1 0))
  (setv UP (Vector 0 -1))
  (setv STOP (Vector 0 0))
  (setv RIGHT (Vector 1 0))

  (with-decorator staticmethod
    (defn list []
      [Move.DOWN Move.LEFT Move.UP Move.STOP Move.RIGHT]
    )
  )
)

(defclass parsing []
  (with-decorator staticmethod
    (defn get_position [^np.ndarray values ^str value]
      (setv coords (np.nonzero (= values value)))
      (setv coords (lfor coord (cut coords None None -1) (coord.item)))
      (Position (unpack-iterable coords))
    )
  )
  (with-decorator staticmethod
    (defn read_layout [^str path]
      (with [file (open path)]
        (setv layout (lfor line file (list (line.strip))))
      )
      (np.array layout)
    )
  )
  (with-decorator staticmethod
    (defn load_layout [^str path]
      (setv layout (Parser.read_layout path))
      (setv labyrinth (= layout "#"))
      (setv player (Parser.get_position layout "P"))
      (setv invader(Parser.get_position layout "G"))
      (, maze [lasers])
    )
  )
)

(with-decorator (dataclass :eq False)
  (defclass State []
    (^Labyrinth labyrinth)
    (^(of list Position) agents)
    (setv ^(of tuple Agent Vector) last_move None)

    (with-decorator property
      (defn player [self]
        (get self.agents 0)
      )
    )
    (with-decorator property
      (defn lasers [self]
        (get self.agents 1)
      )
    )
    (with-decorator property
      (defn game_over [self]
        (= self.player self.invader)
      )
    )
    (defn selectMoves [self ^Agent agent]
      (setv position (get self.agents agent))
      (setv moves [])
      (for [move (Move.list)]
        (setv (, xx yy) (+ position move))
        (if-not (get (get self.labyrinth yy) xx)
          (moves.append move)
        )
      )
      moves
    )
    (defn generateNext [self ^Agent agent ^Vector move]
      (setv new_agents (lfor agent self.agents (agent.copy)))
      (setv new_lab (self.labyrinth.copy))
      (setv position (get self.agents agent))
      (setv (get new_agents agent) (+ position move))
      (State new_maze new_agents (, agent move))
    )
  )
)

(with-decorator (dataclass :eq False)
  (defclass MinimaxState []
    (^State game)
    (setv ^Agent agent 0)
    (setv ^int depth 0)

    (with-decorator property
      (defn move [self]
        (get (. self.game last_move) 1)
      )
    )
  )
)

(with-decorator (dataclass :eq False)
  (defclass MinimaxValue []
    (^int cost)
    (setv ^Vector move Move.STOP)
  )
)

(with-decorator (dataclass :eq False)
  (defclass Minimax []
    (setv ^int max_depth 2)

    (defn getNeighbors [self ^MinimaxState state]
      (setv depth (if (= state.agent 0) state.depth (+ state.depth 1)))
      (setv agent (% (+ state.agent 1) 2))

      (setv game state.game)
      (gfor move (game.get_moves state.agent)
        :do (setv next_game (game.generate_next state.agent move))
        (MinimaxState next_game agent depth)
      )
    )
    (defn utility [self ^MinimaxState state]
      (if (. state.game game_over)
        (return (float "inf"))
      )
      (setv player (. state.game player))
      (setv invader (. state.game invader))
      (pacman.manhattan invader)
    )
    (defn is_terminal [self ^MinimaxState state]
      (or (. state.game game_over) (= state.depth self.max_depth))
    )
    (defn minimax [self ^MinimaxState state]
      (if (self.is_terminal state) (MinimaxValue (self.utility state))
          (= state.agent 0) (self.max_value state)
          (self.min_value state)
      )
    )
    (defn min_value [self ^MinimaxState state]
      (setv values
        (lfor neighbor (self.get_neighbors state)
          (MinimaxValue (. (self.minimax neighbor) cost) neighbor.move)
        )
      )
      (setv value (min values :key (fn [neighbor] neighbor.cost)))
      value
    )
    (defn max_value [self ^MinimaxState state]
      (setv values
        (lfor neighbor (self.get_neighbors state)
          (MinimaxValue (. (self.minimax neighbor) cost) neighbor.move)
        )
      )
      (setv value (max values :key (fn [neighbor] neighbor.cost)))
      value
    )
    (defn __call__ [self ^State state]
      (. (self.minimax (MinimaxState state)) move)
    )
  )
)

(print "Player and Invader: " agents)
(setv state (State labyrinth agents))
(setv minimax (Minimax 2))
(setv best_move (minimax state))
(print "Best Move: " best_move)